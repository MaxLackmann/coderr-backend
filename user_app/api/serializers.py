from rest_framework import serializers
from user_app.models import CustomUser
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password  = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise ValidationError({"password": ["Passwörter stimmen nicht überein."]})

        return attrs
    
    def create(self, validated_data):
        validated_data.pop('repeated_password', None)
        try:
            return CustomUser.objects.create_user(**validated_data)
        except IntegrityError as e:
            if 'email' in str(e):
                raise ValidationError({"email": ["e-mail existiert bereis."]})
            elif 'username' in str(e):
                raise ValidationError({"username": ["username existiert bereits."]})
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
            attrs["user"] = user
            return attrs

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"details": ["username or password nicht korrekt"]})

        if not user.check_password(password):
            raise serializers.ValidationError({"details": ["username or password nicht korrekt"]})

        attrs['user'] = user
        return attrs
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']