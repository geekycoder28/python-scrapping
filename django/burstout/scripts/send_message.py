import pika
import sys
from burstout.models import Channel
from burstout.models import Space
from burstout.models import Message
import json
import random
from uuid import uuid4, UUID
from faker import Faker

import redis
from pprint import pformat, pprint

red = redis.Redis(host='localhost', port=6379, db=0)

fake = Faker()
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
pika_channel = connection.channel()


def send_message():
    pika_channel.exchange_declare(exchange='messages',
                                  exchange_type='direct')

    channel = Channel.objects.get(
        id=UUID("9d4d60aa-b520-40d4-bbfc-44a6964d2fd4"))

    members = channel.members.all()
    rnd_idx = random.randint(1, len(members)) - 1
    source = members[rnd_idx]
    message = Message.objects.create(
        channel=channel,
        body=fake.text(),
        source=source)

    channel.preview = message.body
    channel.preview_datetime = message.creation_datetime
    channel.save()

    message = {
        "id": str(message.id),
        "time": str(message.creation_datetime),
        "source_id": str(source.id),
        "body": str(message.body),
        "avatar": fake.image_url(width=None, height=None)
    }
    red.hset('messages', str(message["id"]), json.dumps(message))
    print("Sending {m}".format(m=pformat(message)))

    message = {
        "id": message["id"],
    }
    pika_channel.basic_publish(exchange='messages',
                               routing_key="all",
                               body=json.dumps(message))


def create_channel():
    pika_channel.exchange_declare(exchange='channels',
                                  exchange_type='direct')

    space = Space.objects.get(
        id=UUID("8458d932-01f8-475a-91bb-9c59fba83a85"))

    members = list(space.members.all())
    channel = Channel.objects.create(space=space)

    num_members = random.randint(1, len(members))
    rand_members = random.sample(members, num_members)

    for member in rand_members:
        channel.members.add(member)

    rnd_idx = random.randint(1, len(members)) - 1
    source = members[rnd_idx]

    r_channel = {
        "id": str(channel.id),
        "time": str(channel.creation_datetime),
        "request_id": str(uuid4())
    }
    red.hset('channels', str(r_channel["id"]), json.dumps(r_channel))
    pika_channel.basic_publish(exchange='channels',
                               routing_key="all",
                               body=json.dumps(r_channel))

    message = Message.objects.create(
        channel=channel,
        body=fake.text(),
        source=source)

    channel.preview = message.body
    channel.preview_datetime = message.creation_datetime
    channel.save()

    message = {
        "id": str(message.id),
        "time": str(message.creation_datetime),
        "source_id": str(source.id),
        "body": str(message.body),
        "avatar": fake.image_url(width=None, height=None)
    }
    red.hset('messages', str(message["id"]), json.dumps(message))
    print("Sending {m}".format(m=pformat(message)))

    message = {
        "id": message["id"],
    }
    pika_channel.basic_publish(exchange='messages',
                               routing_key="all",
                               body=json.dumps(message))


def run():
    # send_message()
    create_channel()
    connection.close()
