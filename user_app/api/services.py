from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from user_app.models import CustomUser, GuestToken

class UserService:
    @staticmethod
    def register_user(validated_data):
        """
        Registers a user using the validated_data dictionary.

        :param validated_data: A dictionary of validated user attributes
        :return: The newly created CustomUser object
        """

        validated_data.pop('repeated_password', None)
        return CustomUser.objects.create_user(**validated_data)

    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticates a user using a username and password.

        Allows guest users to be created if the username is in the GUEST_USERS dictionary
        and the password matches the one in the dictionary.

        Otherwise, it uses the default django.contrib.auth.authenticate function.

        :param username: The username to authenticate with
        :param password: The password to authenticate with
        :return: A CustomUser object if authentication is successful, None if not
        """

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
        """
        Generate a token for the given user.

        If the user is a guest (username in ["andrey", "kevin"]), a new GuestToken
        is created with a random key. Otherwise, a regular Token is created or
        reused.

        :param user: The user for which the token should be generated.
        :return: The generated token.
        """

        if user.username in ["andrey", "kevin"]:
            token = GuestToken.objects.create(user=user, key=get_random_string(40))
        else:
            token, _ = Token.objects.get_or_create(user=user)
        return token.key

    @staticmethod
    def get_filtered_profiles(user_type):
        """
        Retrieve a list of profiles filtered by type.

        :param user_type: The type of user to filter by.
        :return: A queryset of user profiles.
        """

        return CustomUser.objects.filter(type=user_type)

    @staticmethod
    def get_profile(pk):
        """
        Retrieve a user profile by its primary key.

        :param pk: The primary key of the user to retrieve.
        :return: The user instance.
        :raises: Http404 if the user does not exist.
        """

        return CustomUser.objects.get(pk=pk)