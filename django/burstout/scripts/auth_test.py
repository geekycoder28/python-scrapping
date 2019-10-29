from burstout.models import UserManager
from burstout.AuthBackEnd import AuthBackEnd
from faker import Faker
import random
fake = Faker()


def run():
    auth_backend = AuthBackEnd()
    user_manager = UserManager()

    print(auth_backend.authenticate(None, username, phone_number, password))
    print(auth_backend.authenticate(None, None, phone_number, password))

    wrong_password = fake.password(
        length=random.randint(10, 32), special_chars=True, digits=True, upper_case=True, lower_case=True)
    print(auth_backend.authenticate(None, username, phone_number, wrong_password))
