from rest_framework import serializers
from user_app.models import CustomUser
import re

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('business', 'Business'), ('customer', 'Customer')])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, attrs):
        """
        Validates the input attributes for registration.
    
        Ensures that the password and repeated_password fields match.
    
        Args:
            attrs (dict): A dictionary of attributes to validate.
    
        Returns:
            dict: The validated attributes.
    
        Raises:
            serializers.ValidationError: If the passwords do not match.
        """

        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError({"detail": ["Passwörter stimmen nicht überein."]})
        return attrs
    
    def validate_email(self, email):
        """
        Validates the email field.
    
        Ensures that the email is unique.
    
        Args:
            email (str): The email to validate.
    
        Returns:
            str: The validated email.
    
        Raises:
            serializers.ValidationError: If the email is not unique.
        """
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"detail": ["Überprüfe deine Angaben."]})
        return email
    
    def validate_username(self, username):
        """
        Validates the username field.

        Ensures that the username is unique.

        Args:
            username (str): The username to validate.

        Returns:
            str: The validated username.

        Raises:
            serializers.ValidationError: If the username is not unique.
        """

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({"detail": ["Überprüfe deine Angaben."]})
        return username

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """
        Validates the username and password.
    
        Checks if the username is in the list of guest users. If it is, creates the user if it does not exist.
        If the user is not in the list of guest users, checks if the username and password match a user in the database.
    
        Args:
            attrs (dict): The validated data.
    
        Returns:
            dict: The validated data with the user added to it.
    
        Raises:
            serializers.ValidationError: If the username or password is invalid.
        """

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
            raise serializers.ValidationError({"detail": ["username oder password nicht korrekt"]})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": ["username oder password nicht korrekt"]})

        attrs['user'] = user
        return attrs
    
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']

    def validate_email(self, email):
        """
        Validate the 'email' field to ensure it is unique among all users.

        Args:
            email (str): The email address to validate.

        Raises:
            serializers.ValidationError: If the email address is already taken.
        """

        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"detail": ["Diese E-Mail ist bereits vergeben."]})
        return email

    def validate_tel(self, tel):
        """
        Validate the 'tel' field to ensure it is unique among all users and matches the correct format.

        The format is defined by the regular expression '^\d\s\-\+\(\]+$' which allows for digits, spaces, hyphen, plus, and parentheses.

        :param tel: The telephone number to validate.
        :return: The validated telephone number.

        Raises:
            serializers.ValidationError: If the telephone number is invalid or already taken.
        """
        phone_regex = re.compile(r'^[\d\s\-\+\(\)]+$')

        if not phone_regex.match(tel):
            raise serializers.ValidationError({"detail": ["Telefonnummer darf nur Ziffern und die Zeichen '+', '-', '()', und Leerzeichen enthalten."]})

        if CustomUser.objects.filter(tel=tel).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"detail": ["Diese Telefonnummer ist bereits vergeben."]})

        return tel

class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

    def get_user(self, obj):
        """
        Returns a dictionary containing the id, username, first name and last name of the user.

        Args:
            obj (CustomUser): The user instance.

        Returns:
            dict: A dictionary containing the id, username, first name and last name of the user.
        """

        return {
            "pk": obj.id,
            "username": obj.username,
            "first_name": obj.first_name or "",
            "last_name": obj.last_name or ""
        }
    
class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user', 'file', 'type']

    def get_user(self, obj):
        """
        Returns a dictionary containing the id, username, first name and last name of the user.

        Args:
            obj (CustomUser): The user instance.

        Returns:
            dict: A dictionary containing the id, username, first name and last name of the user.
        """
        
        return {
            "pk": obj.id,
            "username": obj.username,
            "first_name": obj.first_name or "",
            "last_name": obj.last_name or ""
        }
