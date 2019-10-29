from django.db.models import CharField, Model, UUIDField, BooleanField, DateTimeField
from django.db.models import CASCADE, PROTECT
from django.db.models import OneToOneField, ForeignKey, ManyToManyField, TextField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
from uuid import uuid4
from pprint import pformat
import json
from django.contrib.auth import get_user_model


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_name, phone_number, password, display_name, image_url):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not user_name:
            raise ValueError('Users must have a user_name')

        space = Space.objects.create(
            domain_name=user_name + ".x.com", is_default=True)
        User = get_user_model()

        home_room = Channel.objects.create(
            channel_name=display_name + "'s Home")

        user = User(user_name=user_name, phone_number=phone_number,
                    display_name=display_name, image_url=image_url, space=space,
                    home_room=home_room)



        user.set_password(password)
        user.save()

        home_room.members.add(user)
        return user


class User(AbstractBaseUser):
    id = UUIDField(
        primary_key=True, default=uuid4, editable=False)
    creation_datetime = DateTimeField(now, auto_now_add=True, editable=False)
    phone_number = PhoneNumberField(unique=True)
    user_name = CharField(max_length=32, unique=True)
    display_name = CharField(max_length=64, unique=False)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    is_private = BooleanField(default=False)
    image_url = CharField(max_length=128, unique=False)
    biography = CharField(max_length=128, unique=False)
    space = OneToOneField("Space", on_delete=PROTECT)
    connections = ManyToManyField("self")
    home_room = OneToOneField("Channel", on_delete=PROTECT)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['user_name', 'phone_number', "name"]

    def __str__(self):
        obj_dict = {"id": str(self.id), "user_name": self.user_name}
        json_str = json.dumps(obj_dict, sort_keys=True,
                              indent=4, separators=(',', ': '))
        return "User : {o}".format(o=json_str)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Organization(AbstractBaseUser):
    id = UUIDField(
        primary_key=True, default=uuid4, editable=False)
    creation_datetime = DateTimeField(now, auto_now_add=True, editable=False)
    display_name = CharField(max_length=64, unique=False)
    space = OneToOneField("Space", on_delete=PROTECT)
    image_url = CharField(max_length=128, unique=False)
    description = CharField(max_length=128, unique=False)
    is_private = BooleanField(default=False)
    members = ManyToManyField(User)

    def __str__(self):
        obj_dict = {"id": str(self.id),
                    "creation_datetime": str(self.creation_datetime),
                    "display_name": self.display_name,
                    "image_url": self.image_url,
                    "is_private": self.is_private}
        json_str = json.dumps(obj_dict, sort_keys=True,
                              indent=4, separators=(',', ': '))
        return "Organization : {o}".format(o=json_str)


class Space(Model):
    id = UUIDField(
        primary_key=True, default=uuid4, editable=False)
    creation_datetime = DateTimeField(now, auto_now_add=True, editable=False)
    space_name = CharField(max_length=32, unique=False)
    display_name = CharField(max_length=64, unique=False)
    domain_name = CharField(max_length=256, unique=True, blank=True)
    is_private = BooleanField(default=False)
    is_default = BooleanField(default=False)
    channels = ManyToManyField("Channel")

    def __str__(self):
        obj_dict = {"id": str(self.id),
                    "creation_datetime": str(self.creation_datetime),
                    "space_name": self.space_name,
                    "display_name": self.display_name,
                    "is_private": self.is_private,
                    "is_default": self.is_default}
        json_str = json.dumps(obj_dict, sort_keys=True,
                              indent=4, separators=(',', ': '))
        return "Space : {o}".format(o=json_str)


class Channel(Model):
    id = UUIDField(
        primary_key=True, default=uuid4, editable=False)
    creation_datetime = DateTimeField(now, auto_now_add=True, editable=False)
    members = ManyToManyField(User)
    channel_name = CharField(max_length=128, unique=False)

    def __str__(self):
        obj_dict = {"id": str(self.id),
                    "creation_datetime": str(self.creation_datetime),
                    "members": str(list(self.members.all()))}
        json_str = json.dumps(obj_dict, sort_keys=True,
                              indent=4, separators=(',', ': '))
        return "Channel : {o}".format(o=json_str)


class Message(Model):
    id = UUIDField(
        primary_key=True, default=uuid4, editable=False)
    creation_datetime = DateTimeField(now, auto_now_add=True, editable=False)
    channel = ForeignKey(Channel, on_delete=PROTECT)
    body = TextField()
    source = ForeignKey(User, on_delete=PROTECT)
    request_id = UUIDField(null=True, editable=False, unique=True)

    def __str__(self):
        s = "Message id: {id} creation_datetime time: {ct}".format(
            id=str(self.id), ct=self.creation_datetime)
        return s
