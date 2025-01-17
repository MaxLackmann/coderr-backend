from rest_framework import serializers
from user_app.models import CustomUser
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now
from ..models import GuestToken

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password  = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise ValidationError({"password": "Passwords do not match."})

        return attrs
    
    def create(self, validated_data):
        validated_data.pop('repeated_password', None)
        try:
            return CustomUser.objects.create_user(**validated_data)
        except IntegrityError as e:
            if 'email' in str(e):
                raise ValidationError({"email": ["e-mail already exists."]})
            elif 'username' in str(e):
                raise ValidationError({"username": ["username already exists."]})
            raise
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        GUEST_USERS = {
            "andrey": {"password": "asdasd", "type": "customer"},
            "kevin": {"password": "asdasd24", "type": "business"},
        }

        if username in GUEST_USERS and password == GUEST_USERS[username]["password"]:
            user, _ = CustomUser.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@guest.com", "type": GUEST_USERS[username]["type"]}
            )

            GuestToken.objects.filter(user=user, expires_at__lt=now()).delete()

            token = GuestToken.objects.create(user=user)
            return {
                "user": user,
                "token": token.key,
            }

        if username and password:
            user = CustomUser.objects.filter(username=username).first()
            if not user:
                raise serializers.ValidationError("Username does not exist.")
        
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password.")

        attrs['user'] = user
        return attrs