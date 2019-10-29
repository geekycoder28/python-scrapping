from pymongo import MongoClient
from burstout.models import Message
from burstout.models import Channel
from burstout.models import Space
from burstout.models import Organization
from burstout.models import User
from burstout.models import UserManager
from burstout.AuthBackEnd import AuthBackEnd
from django.db.models import ProtectedError
from django.db.utils import IntegrityError
from os import environ
import json
import math
import random
import phonenumbers
import requests
from pprint import pprint

from faker import Faker
fake = Faker()

mongodb = MongoClient()

mongo_users = mongodb["burstout"]["users"]
mongo_orgs = mongodb["burstout"]["organizations"]
mongo_channels= mongodb["burstout"]["channels"]
mongo_messages= mongodb["burstout"]["messages"]
mongo_spaces= mongodb["burstout"]["spaces"]

NUM_USERS = 10
NUM_ORGS = 3
NUM_CHAN = 30
NUM_MSG = 200


def delete_objects(model, key):
    print("Deleting {k}".format(k=key))
    try:
        objs = model.objects.all()
        objs.delete()
    except ProtectedError:
        error_message = "Some {k} objects can't be deleted!!".format(k=key)
        print(error_message)

    mongodb["burstout"][key].drop()



def delete_all():
    delete_objects(Message, "messages")
    delete_objects(Space, "spaces")
    delete_objects(Channel, "channels")
    delete_objects(Organization, "organizations")
    delete_objects(User, "users")


def init_users():
    print("Initializing Users")
    user_manager = UserManager()

    res = requests.get("https://randomuser.me/api?results={n}".format(n=NUM_USERS))

    for rand_user in res.json()["results"]:
        user_name = rand_user["login"]["username"]
        display_name = "{f} {l}".format(f=rand_user["name"]["first"], l=rand_user["name"]["last"]).title()
        phone_number = phonenumbers.parse(fake.phone_number(), "US")
        biography = random.choice([fake.job(), fake.text(max_nb_chars=128, ext_word_list=None)])

        password = fake.password(
            length=random.randint(5, 10), special_chars=False, digits=True, upper_case=True, lower_case=True)

        image_url = rand_user["picture"]["large"]

        user_list = list(User.objects.all())
        num_connections = random.randint(0, math.floor(2*math.sqrt(NUM_USERS)))
        rand_connections = random.sample(user_list, min(len(user_list), num_connections))



        user = user_manager.create_user(
            user_name, phone_number, password, display_name, image_url=image_url)


        connection_ids = [c.id for c in rand_connections]
        connections = list(User.objects.filter(id__in=connection_ids))
        user.connections.add(*connections)
        user.biography = biography

        user.save()

        print("Created user: {u}".format(
            u=str(user)))

        r_user = {
            "id": str(user.id),
            "display_name": str(user.display_name),
            "user_name": str(user.user_name),
            "biography": str(user.biography),
            "password": str(password),
            "image_url": str(user.image_url),
        }
        mongo_users.insert_one(r_user)


def init_orgs():
    print("Initializing external spaces")
    user_list = list(User.objects.all())

    for i in range(NUM_ORGS):
        try:
            num_members = random.randint(1, 1 + int(NUM_USERS / NUM_ORGS) * 2)
            rand_members = random.sample(user_list, num_members)

            space_name = fake.user_name()
            display_name = fake.company()
            domain_name = fake.domain_name()
            image_url = "http://lorempixel.com/512/512/abstract/"
            description = fake.text(max_nb_chars=128, ext_word_list=None)

            space = Space.objects.create(
                is_default=False,
                space_name=space_name,
                display_name=display_name,
                domain_name=domain_name)

            org = Organization.objects.create(
                display_name=display_name,
                space=space,
                description=description,
                image_url=image_url)

            org.members.set(rand_members)

            space = {
                "id": str(space.id),
                "image_url": str(image_url),
                "creation_datetime": str(space.creation_datetime),
                "space_name": str(space.space_name),
                "display_name": str(space.display_name),
                "domain_name": str(space.domain_name),
            }
            mongo_spaces.insert_one(space)

            org = {
                "id": str(org.id),
                "image_url": str(org),
                "creation_datetime": str(org.creation_datetime),
                "description": str(org.description),
                "display_name": str(org.display_name),
            }
            mongo_users.insert_one(org)
        except IntegrityError as ie:
            print("IntegrityError", ie)


def init_channels():

    print("Initializing channels")
    user_list = list(User.objects.all())

    for i in range(NUM_CHAN):
        channel_name = fake.text(max_nb_chars=128)
        channel = Channel.objects.create(channel_name=channel_name)

        num_members = random.randint(1, len(user_list))
        rand_members = random.sample(user_list, num_members)

        for member in rand_members:
            channel.members.add(member)
            member.space.channels.add(channel)


        channel = {
            "id": str(channel.id),
            "time": str(channel.creation_datetime)
        }
        mongo_channels.insert_one(channel)


def init_messages():
    print("Initializing messages")

    channel_list = list(Channel.objects.all())

    # Add a message to every channel
    for i in range(len(channel_list)):
        channel = channel_list[i]
        members = channel.members.all()
        if len(members) <= 1:
            continue
        rnd_idx = random.randint(1, len(members)) - 1
        source = members[rnd_idx]
        message = Message.objects.create(
            channel=channel,
            body=fake.text(),
            source=source)

        channel.preview = message
        channel.save()

        message = {
            "id": str(message.id),
            "time": str(message.creation_datetime),
            "source_id": str(source.id),
            "body": str(message.body),
            "avatar": fake.image_url(width=None, height=None)
        }
        mongo_messages.insert_one(message)

    for i in range(NUM_MSG):
        rnd_idx = random.randint(1, len(channel_list)) - 1
        channel = channel_list[rnd_idx]

        members = channel.members.all()
        if len(members) <= 1:
            continue
        rnd_idx = random.randint(1, len(members)) - 1
        source = members[rnd_idx]
        message = Message.objects.create(
            channel=channel,
            body=fake.text(),
            source=source)

        channel.preview = message
        channel.save()

        message = {
            "id": str(message.id),
            "time": str(message.creation_datetime),
            "source_id": str(source.id),
            "body": str(message.body),
            "avatar": fake.image_url(width=None, height=None)
        }
        mongo_messages.insert_one(message)

def init_cards():
    print("Init card")


def run():
    # delete_all()
    # init_users()
    # init_orgs()
    # init_channels()
    # init_messages()
    init_cards()
