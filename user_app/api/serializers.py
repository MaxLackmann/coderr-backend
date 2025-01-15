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
            raise ValidationError({"password": "Passwords do not match."})

        return attrs
    
    def create(self, validated_data):
        validated_data.pop('repeated_password', None)
        try:
            return CustomUser.objects.create_user(**validated_data)
        except IntegrityError as e:
            # Prüfe, ob der Fehler von einer einzigartigen Einschränkung kommt
            if 'email' in str(e):
                raise ValidationError({"email": ["Diese E-Mail-Adresse wird bereits verwendet."]})
            elif 'username' in str(e):
                raise ValidationError({"username": ["Dieser Benutzername ist bereits vergeben."]})
            raise
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = CustomUser.objects.filter(username=username).first()
            if not user:
                raise serializers.ValidationError("Username does not exist.")
        
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password.")

        attrs['user'] = user
        return attrs