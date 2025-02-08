from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from user_app.models import CustomUser, GuestToken
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now

class UserService:
    @staticmethod
    def register_user(validated_data):
        validated_data.pop('repeated_password', None)
        return CustomUser.objects.create_user(**validated_data)

    @staticmethod
    def authenticate_user(username, password):
        GUEST_USERS = {
            "andrey": {"password": "asdasd", "type": "customer"},
            "kevin": {"password": "asdasd24", "type": "business"},
        }

        if username in GUEST_USERS and password == GUEST_USERS[username]["password"]:
            user, _ = CustomUser.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@guest.com", "type": GUEST_USERS[username]["type"]}
            )
            return user

        return authenticate(username=username, password=password)

    @staticmethod
    def generate_token(user):
        if user.username in ["andrey", "kevin"]:
            token = GuestToken.objects.create(user=user, key=get_random_string(40))
        else:
            token, _ = Token.objects.get_or_create(user=user)
        return token.key

    @staticmethod
    def get_filtered_profiles(user_type):
        return CustomUser.objects.filter(type=user_type)

    @staticmethod
    def get_profile(user_id):
        return CustomUser.objects.get(pk=user_id)