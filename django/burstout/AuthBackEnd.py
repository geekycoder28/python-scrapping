from django.conf import settings
from django.contrib.auth.hashers import check_password
from burstout.models import User


class AuthBackEnd:
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, user_name=None, phone_number=None, password=None):
        try:
            if user_name:
                user = User.objects.get(user_name=user_name)
            elif phone_number:
                user = User.objects.get(phone_number=phone_number)
            else:
                return None
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            print("User Does Not exist!")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
