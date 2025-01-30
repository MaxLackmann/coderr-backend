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
        """Erstellt einen neuen Benutzer."""
        validated_data.pop('repeated_password', None)
        try:
            return CustomUser.objects.create_user(**validated_data)
        except IntegrityError as e:
            if 'email' in str(e):
                raise ValidationError({"email": ["E-Mail existiert bereits."]})
            elif 'username' in str(e):
                raise ValidationError({"username": ["Username existiert bereits."]})
            raise

    @staticmethod
    def authenticate_user(username, password):
        """Authentifiziert einen User (inkl. Gäste)."""
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

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError({"details": ["Username oder Passwort nicht korrekt."]})
        return user

    @staticmethod
    def generate_token(user):
        """Erstellt ein Auth-Token (normal oder Gast)."""
        if user.username in ["andrey", "kevin"]:
            token = GuestToken.objects.create(user=user, key=get_random_string(40))
        else:
            token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_filtered_profiles(user_type):
        """Gibt alle Profile mit bestimmtem Typ zurück (business oder customer)."""
        if user_type not in ["business", "customer"]:
            raise ValidationError({"detail": "Ungültiger User-Typ"})
        return CustomUser.objects.filter(type=user_type)

    @staticmethod
    def get_profile(user_id):
        """Holt ein einzelnes Benutzerprofil anhand der ID."""
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError({"detail": ["User nicht gefunden."]})