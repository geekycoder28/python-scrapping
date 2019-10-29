import main_pb2_grpc
import main_pb2
"""The Python implementation of the gRPC route guide server."""

from burstout.models import Message
from burstout.models import User
from burstout.models import Space
from burstout.models import Channel
from burstout.models import Organization
from burstout.AuthBackEnd import AuthBackEnd
from burstout.models import UserManager
from django.contrib.auth import authenticate, login
from django.db.models import Count
import phonenumbers
from django.db.utils import IntegrityError
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import traceback
from concurrent import futures
import time
import datetime
import math
import logging
import json
import random
import threading
from uuid import uuid4, UUID
from faker import Faker
import pika
import sys
from queue import Queue
import redis
import grpc
from pprint import pprint

current_milli_time = lambda: int(round(time.time() * 1000))

# Your Account SID from twilio.com/console
twilio_TWILIO_ACCOUNT_SID = "AC0cb509ad66d21f69f2fd6e4b566e2449"
# Your Auth Token from twilio.com/console
twilio_auth_token = "5a0b0ee2cd642085b9a2a1e244f938ae"

red = redis.Redis(host='localhost', port=6379, db=0)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def register_servicer(server):
    # with open('/home/peter/grpc_keys/key.pem', 'rb') as f:
    #     private_key = f.read()
    # with open('/home/peter/grpc_keys/certificate.pem', 'rb') as f:
    #     certificate_chain = f.read()
    #
    # server_credentials = grpc.ssl_server_credentials(
    #     ((private_key, certificate_chain), ))
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=32))
    # main_pb2_grpc.add_MainInterfaceServicer_to_server(
    #     MainInterfaceServicer(), server)
    main_pb2_grpc.add_MainInterfaceServicer_to_server(
        MainInterfaceServicer(), server)


def create_space(space):
    channels = space.channels.all()
    channels = map(lambda c: main_pb2.UUID(value=str(c.id)), channels)
    return main_pb2.Space(
        id=main_pb2.UUID(value=str(space.id)),
        creation_timestamp=space.creation_datetime.timestamp(),
        is_default=space.is_default,
        space_name=space.space_name,
        channels=channels,
        display_name=space.display_name)


def create_event(event, event_type=None):
    if event_type in ["HEALTH_CHECK", "CANCEL"]:
        print(event["id"])
        return main_pb2.Event(
            id=main_pb2.UUID(value=event["id"]),
            type=event_type)
    elif event_type in ["ENTER_ROOM"]:
        print("create_event", event)
        return main_pb2.Event(
            id=main_pb2.UUID(value=event["id"]),
            request_id=main_pb2.UUID(value=event["request_id"]),
            user_id=main_pb2.UUID(value=event["user_id"]),
            room_id=main_pb2.UUID(value=event["room_id"]),
            type=event_type)
    elif event_type in ["CREATE_MESSAGE"]:
        message = Message.objects.get(
            id=event["id"])
        return main_pb2.Event(
            id=main_pb2.UUID(value=event["id"]),
            message=create_message(message),
            request_id=main_pb2.UUID(value=event["request_id"]),
            type="RECEIVE_MESSAGE")
    elif event_type in ["CREATE_CHANNEL"]:
        channel = Channel.objects.get(
            id=event["id"])
        return main_pb2.Event(
            id=main_pb2.UUID(value=event["id"]),
            channel=create_channel(channel),
            request_id=main_pb2.UUID(value=event["request_id"]),
            type="RECEIVE_CHANNEL")
    else:
        print("Unknown event_type", event)


def create_channel(channel, request_id=None):

    message_count = channel.message_set.count()
    members = channel.members.all()
    members = map(lambda m: main_pb2.UUID(
        value=str(m.id)), members)

    channel = main_pb2.Channel(
        id=main_pb2.UUID(value=str(channel.id)),
        # preview_id=main_pb2.UUID(value=str(channel.preview.id)),
        members=members,
        channel_name=channel.channel_name,
        message_count=message_count,
        creation_datetime=channel.creation_datetime.replace(
            tzinfo=datetime.timezone.utc).isoformat(),
        creation_timestamp=channel.creation_datetime.timestamp())

    if request_id:
        channel.request_id.CopyFrom(main_pb2.UUID(value=str(request_id)))
    return channel

def create_message(message):
    channel = message.channel
    source = message.source
    return main_pb2.Message(
        body=message.body,
        id=main_pb2.UUID(value=str(message.id)),
        request_id=main_pb2.UUID(value=str(message.request_id)),
        source_id=main_pb2.UUID(value=str(source.id)),
        channel_id=main_pb2.UUID(value=str(channel.id)),
        creation_datetime=message.creation_datetime.replace(
            tzinfo=datetime.timezone.utc).isoformat(),
        creation_timestamp=message.creation_datetime.timestamp())

def create_scan_results(start_index, end_index,
        messages=None, channels=None, users=None):

    result = main_pb2.ScanResult(
        start_index=start_index,
        end_index=end_index)

    if messages:
        result.messages.MergeFrom([create_message(m) for m in messages])

    if channels:
        result.channels.MergeFrom([create_channel(c) for c in channels])

    if users:
        result.users.MergeFrom([create_user(u) for u in users])

    return result



def create_user(user):
    connections = user.connections.all()
    organizations = user.organization_set.all()
    connections = map(lambda c: main_pb2.UUID(
        value=str(c.id)), connections)
    organizations = map(lambda o: main_pb2.UUID(
        value=str(o.id)), organizations)

    return main_pb2.User(
        user_name=user.user_name,
        space=main_pb2.UUID(value=str(user.space.id)),
        home_room=main_pb2.UUID(value=str(user.home_room.id)),
        display_name=user.display_name,
        image_url=user.image_url,
        connections=connections,
        biography=user.biography,
        organizations=organizations,
        phone_number=str(user.phone_number),
        id=main_pb2.UUID(value=str(user.id)),
        creation_datetime=user.creation_datetime.replace(
            tzinfo=datetime.timezone.utc).isoformat(),
        creation_timestamp=user.creation_datetime.timestamp())


class MainInterfaceServicer(main_pb2_grpc.MainInterfaceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        print("Initialized MainInterfaceServicer")

    def user_space_scan(self, user_id, context):
        try:
            id = user_id.value
            user = User.objects.get(id=id)

            spaces = list(user.space_set.all())

            for space in spaces:
                yield create_space(space)

        except Exception as e:
            print("Error in user_space_scan", e)
            traceback.print_exc(file=sys.stdout)

    def get_organization(self, org_id, context):
        try:
            org_id = org_id.value
            org = Organization.objects.get(id=org_id)
            members = org.members.all()
            members = map(lambda m: main_pb2.UUID(
                value=str(m.id)), members)
            return main_pb2.Organization(id=str(org.id), display_name=org.display_name, image_url=org.image_url, members=members)

        except Exception as e:
            print("Error in get_organization", e)
            traceback.print_exc(file=sys.stdout)

    def get_user(self, user_id, context):
        try:
            user_id = user_id.value
            user = User.objects.get(id=user_id)
            return create_user(user)

        except Exception as e:
            print("Error in get_user", e)
            traceback.print_exc(file=sys.stdout)

    def get_user_batch(self, cursor, context):
        try:
            if cursor.id_list:
                print("xxxx")
            length = cursor.length
            limit = cursor.limit
            users = User.objects.all()[:limit]
            print(length, limit, len(users))

            for i in range(int(len(users)/length) + 1):

                start_idx = i * length
                end_idx = (i+1) * length
                yield create_scan_results(
                    start_index=start_idx,
                    end_index=end_idx,
                    users=users[start_idx:end_idx])

        except Exception as e:
            print("Error in get_user", e)
            traceback.print_exc(file=sys.stdout)

    def get_user_twilio_token(self, user_id, context):
        try:
            user_id = user_id.value
            # print("get_user_twilio_token", user_id)

            TWILIO_ACCOUNT_SID = 'AC0cb509ad66d21f69f2fd6e4b566e2449'
            TWILIO_API_KEY_SID = 'SK6ea1006b0adabde2957b9077e0a25679'
            TWILIO_API_KEY_SECRET = 'AP6uPE2wJoVACZlWG2CSnDBI40MRaYfM'

            # Create an Access Token
            token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET)

            # Set the Identity of this token
            token.identity = user_id

            # Grant access to Video
            grant = VideoGrant(room='AwesomeRoom')
            token.add_grant(grant)

            # Serialize the token as a JWT
            jwt = token.to_jwt().decode('utf-8')

            print(jwt)
            print(user_id)
            print(token.payload["exp"])

            return main_pb2.JWTToken(
                id=main_pb2.UUID(value=str(user_id)),
                expiry_time=token.payload["exp"],
                jwt=jwt)

        except Exception as e:
            print("Error in get_user", e)
            traceback.print_exc(file=sys.stdout)

    def get_space(self, space_id, context):
        try:
            space_id = space_id.value
            space = Space.objects.get(id=space_id)
            return create_space(space)

        except Exception as e:
            print("Error in get_user", e)
            traceback.print_exc(file=sys.stdout)

    def get_channel(self, channel_id, context):
        try:
            print("!!!!")
            channel_id = channel_id.value
            channel = Channel.objects.get(id=channel_id)
            return create_channel(channel)

        except Exception as e:
            print("Error in channel", e)
            traceback.print_exc(file=sys.stdout)

    def get_message(self, message_id, context):
        try:
            message_id = message_id.value
            message = Message.objects.get(id=message_id)
            return create_message(message)

        except Exception as e:
            print("Error in channel", e)
            traceback.print_exc(file=sys.stdout)

    def get_message_batch(self, batch_req, context):
        try:
            id_list = batch_req.id_list
            id_list = [i.value for i in id_list]
            message = Message.objects.filter(id__in=id_list)
            # print(message[:5])
            # return create_message(message)

        except Exception as e:
            print("Error in channel", e)
            traceback.print_exc(file=sys.stdout)

    def channel_message_scan(self, cursor, context):
        try:
            print("Called: channel_message_scan")
            id = cursor.entity_id.value
            channel = Channel.objects.get(id=id)
            messages = channel.message_set.all().order_by(
                "-creation_datetime")
            # messages = reversed(messages)

            for message in messages:
                yield create_message(message)

        except Exception as e:
            print("Error in channel_message_scan", e)
            traceback.print_exc(file=sys.stdout)

    def scan_messages_in_channel(self, cursor, context):
        try:
            id = cursor.entity_id.value
            length = cursor.length
            limit = cursor.limit
            channel = Channel.objects.get(id=id)
            messages = channel.message_set.all().order_by(
                "-creation_datetime")[:limit]

            for i in range(int(len(messages)/length) + 1):

                start_idx = i * length
                end_idx = (i+1) * length
                yield create_scan_results(
                    start_index=start_idx,
                    end_index=end_idx,
                    messages=messages[start_idx:end_idx])

        except Exception as e:
            print("Error in channel_message_scan", e)
            traceback.print_exc(file=sys.stdout)

    def scan_channels_in_space(self, cursor, context):
        try:
            # print("Called: scan_channels_in_space")
            # print(cursor)
            id = cursor.entity_id.value
            length = cursor.length
            limit = cursor.limit
            space = Space.objects.get(id=id)
            channels = Channel.objects.filter(space=space)[:limit]

            for i in range(int(len(channels)/length) + 1):
                start_idx = i * length
                end_idx = (i+1) * length
                yield create_scan_results(
                    start_index=start_idx,
                    end_index=end_idx,
                    channels=channels[start_idx:end_idx])

        except Exception as e:
            print("Error in space_channel_scan", e)
            traceback.print_exc(file=sys.stdout)

    def event_stream(self, event_iterator, context):
        try:
            print("event_stream ++++++++++++++++++++++++++++++++++")
            queue = Queue()
            NO_ACK_TOLERANCE = 3
            SLEEP_INTERVAL_SEC = 3

            def listener_fn(e, connection_listener):
                # print("Start listener_fn thread")
                pika_channel_listener = connection_listener.channel()
                pika_channel_listener.exchange_declare(exchange='events',
                                              exchange_type='direct')

                result = pika_channel_listener.queue_declare(exclusive=True)
                queue_name = result.method.queue

                pika_channel_listener.queue_bind(exchange='events',
                                        queue=queue_name,
                                        routing_key="all")

                def callback(ch, method, properties, body):
                    try:
                        body = body.decode("utf-8")
                        body = json.loads(body)
                        print("Got event: ThreadId ID", threading.get_ident())
                        pprint(body)
                        queue.put(body)
                        e.set()
                    except:
                        print("Something else went wrong")

                pika_channel_listener.basic_consume(callback,
                                           queue=queue_name,
                                           no_ack=True)

                pika_channel_listener.start_consuming()
                print("stop listener_fn thread")


            def iterator_fn(e, cid=None):
                # print("Start iterator_fn thread")
                try:
                    for event in event_iterator:
                        if event.type == "HEALTH_CHECK_ACK":
                            r = red.zrank(cid, event.id.value)
                            c = red.zremrangebyrank(cid, 0, r)
                            if c < 1:
                                print("Error removing event", event)
                            continue

                        request_id = UUID(event.request_id.value)

                        _event = {
                            "id": str(request_id),
                            "request_id": str(request_id),
                            "type": event.type,
                        }

                        if event.type in ["ENTER_ROOM"]:
                            _event["room_id"] = event.room_id.value
                            _event["user_id"] = event.user_id.value
                            print(_event)
                        elif event.type in ["CREATE_MESSAGE"]:
                            _event["room_id"] = event.room_id.value
                            _event["request_id"] = event.request_id.value
                            _event["source_id"] = event.source_id.value
                            _event["body"] = event.body

                            room = Channel.objects.get(
                                id=event.room_id.value)
                            source = User.objects.get(id=event.source_id.value)
                            message = Message.objects.create(
                                channel=room,
                                body=event.body,
                                source=source,
                                request_id=event.request_id.value)

                            _event["id"] = str(message.id)
                        elif event.type in ["CREATE_CHANNEL"]:
                            _event["request_id"] = event.request_id.value
                            member_ids = map(lambda m: str(m.value), event.members)
                            members = list(User.objects.filter(id__in=member_ids))

                            channel_query = Channel.objects.all().annotate(
                                count=Count('members')).filter(count=len(members))

                            for member in members:
                                channel_query = channel_query.filter(
                                    members=member)

                            if channel_query.count():
                                channel = channel_query.all().first()
                            else:
                                # Create channel if it does not exist.
                                channel_name = "XDSSD"
                                channel = Channel.objects.create(channel_name=channel_name)
                                # For each user, create add the channel to the default space
                                for member in members:
                                    channel.members.add(member)
                                    space = member.space
                                    space.channels.add(channel)
                                    space.save()
                                channel.save()

                            _event["id"] = str(channel.id)


                        else:
                            print("Unknown event!!. Skipping: ", event)
                            continue


                        # Queue the message
                        connection = pika.BlockingConnection(
                            pika.ConnectionParameters(host='localhost'))
                        pika_channel = connection.channel()
                        pika_channel.exchange_declare(
                            exchange='events', exchange_type='direct')
                        pika_channel.basic_publish(exchange='events', routing_key='all', body=json.dumps(_event))
                    print("stop iterator_fn thread")
                    message =  {"type" : "CANCEL"}
                    queue.put(message)
                    e.set()

                except grpc.RpcError as grpcErr:
                    print("Caught grpcErr")
                    print(grpcErr)

            def health_check_fn(e, cid=None):
                # print("Start health_check_fn thread")

                no_ack_cardi = red.zcard(cid)
                while no_ack_cardi <= (NO_ACK_TOLERANCE + 1):
                    _event =  {
                        "id" : str(uuid4()),
                        "type" : "HEALTH_CHECK"
                    }

                    queue.put(_event)
                    red.zadd(cid, {
                        _event["id"] : current_milli_time()})
                    no_ack_cardi = red.zcard(cid)
                    e.set()
                    time.sleep(SLEEP_INTERVAL_SEC)
                print("stop health_check_fn thread")

            thread_event = threading.Event()
            health_check_client_id = "HEALTH_CHECK_CLIENT_ID-" + str(uuid4())
            # print("HEALTH_CHECK_CLIENT_ID: ", health_check_client_id)
            connection_listener = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))

            threads = [
                threading.Thread(
                    target=listener_fn,
                    args=(thread_event, connection_listener,),
                    name="listener_fn"),
                threading.Thread(
                    target=iterator_fn,
                    args=(thread_event,),
                    kwargs={"cid" : health_check_client_id},
                    name="iterator_fn"),
                threading.Thread(
                    target=health_check_fn,
                    args=(thread_event,),
                    kwargs={"cid" : health_check_client_id},
                    name="health_check_fn"),
            ]

            # print("Starting threads ", threading.get_ident())
            [t.start() for t in threads]


            no_ack_cardi = red.zcard(health_check_client_id)
            while no_ack_cardi < NO_ACK_TOLERANCE:
                thread_event.wait()
                event = queue.get()
                if event["type"] in ["CANCEL"]:
                    break
                no_ack_cardi = red.zcard(health_check_client_id)
                yield create_event(event, event_type=event["type"])
                thread_event.clear()

            # print("Stoping threads ", threading.get_ident())
            connection_listener.close()

            try:
                context.abort(grpc.StatusCode.CANCELLED, "Cancelled request. Unrepsonsive client")
            except Exception as e:
                print("Aborted iteration loop")

            [t.join() for t in threads]
            # for t in threads:
            #      print("isAlive: ", t.isAlive(), t.ident, t.getName())

            print("Stoped threads and joined.", threading.get_ident(), current_milli_time())
            return None

        except Exception as e:
            print("Error in event_stream", e)
            traceback.print_exc(file=sys.stdout)

    def auth_login(self, creds, context):
        try:
            print("context", context.peer())
            print("peer_identities", context.peer_identities())
            meta = {}
            for key, value in context.invocation_metadata():
                meta[key] = value
            pprint(meta)

            # User.get(user_name=)

            user_name = creds.identifier
            # user_name = "organicgoose938"
            password = creds.password
            # password = "2YVeskEWV"
            auth_backend = AuthBackEnd()
            user = auth_backend.authenticate(
                None, user_name=user_name, password=password)


            if user:
                user_res = create_user(user)
                auth_res = main_pb2.AuthResult(user=user_res, valid=True)
                print(user_name, user_res, auth_res)
            else:
                auth_res = main_pb2.AuthResult(valid=False)

            return auth_res
        except IntegrityError as e:
            print("IntegrityError in channel_stream", e)
            traceback.print_exc(file=sys.stdout)
            auth_res = main_pb2.AuthResult(valid=False)
        except Exception as e:
            print("Error in channel_stream", e)
            traceback.print_exc(file=sys.stdout)
            auth_res = main_pb2.AuthResult(valid=False)

        return auth_res

    def auth_signup(self, creds, context):
        try:
            name = creds.user.name
            user_name = creds.user.user_name
            phone_number = creds.user.phone_number
            password = creds.password
            _phone_number = phonenumbers.parse(phone_number, None)
            assert "Phone number not possible", phonenumbers.is_possible_number(
                _phone_number)
            assert "Phone number not valid", phonenumbers.is_valid_number(
                _phone_number)

            user_manager = UserManager()
            user = user_manager.create_user(
                user_name=user_name, phone_number=phone_number, password=password, name=name)

            if user:
                user_res = create_user(user)
                auth_res = main_pb2.AuthResult(user=user_res, valid=True)

                r_user = {
                    "id": str(user.id),
                    "name": str(user.name),
                    "user_name": str(user.user_name),
                    "password": str(password),
                }
                red.hset('users', str(r_user["id"]), json.dumps(r_user))
                print("created user {u}".format(u=user))

            else:
                auth_res = main_pb2.AuthResult(valid=False)

            twilio_client = Client(twilio_TWILIO_ACCOUNT_SID, twilio_auth_token)
            verification_code = random.randint(0, 999999)

            message = twilio_client.messages.create(
                to="+13236007994",
                from_="+14243286155",
                body="Welcome to BurstOut. {v} is your verification code".format(v=verification_code))

        except IntegrityError as e:
            print("IntegrityError in channel_stream", e)
            traceback.print_exc(file=sys.stdout)
            auth_res = main_pb2.AuthResult(valid=False)
        except Exception as e:
            print("Error in channel_stream", e)
            traceback.print_exc(file=sys.stdout)
            auth_res = main_pb2.AuthResult(valid=False)

        return auth_res

    def auth_reset(self, creds, context):
        try:
            user_name = creds.user.user_name
            phone_number = creds.user.phone_number
            password = creds.password
            auth_backend = AuthBackEnd()
            user = auth_backend.authenticate(
                None, user_name, phone_number, password)

            if user:
                user_res = create_user(user)
                auth_res = main_pb2.AuthResult(user=user_res, valid=True)
            else:
                auth_res = main_pb2.AuthResult(valid=False)

        except IntegrityError as e:
            print("IntegrityError in channel_stream", e)
            traceback.print_exc(file=sys.stdout)
            auth_res = main_pb2.AuthResult(valid=False)
        except Exception as e:
            print("Error in channel_stream", e)
            traceback.print_exc(file=sys.stdout)
            auth_res = main_pb2.AuthResult(valid=False)

        return auth_res
