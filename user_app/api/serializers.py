from rest_framework import serializers
from user_app.models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('business', 'Business'), ('customer', 'Customer')])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError({"detail": ["Passwörter stimmen nicht überein."]})
        return attrs
    
    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"detail": ["Überprüfe deine Angaben."]})
        return email
    
    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({"detail": ["Überprüfe deine Angaben."]})
        return username

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
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"detail": ["Diese E-Mail ist bereits vergeben."]})
        return email

    def validate_tel(self, tel):
        if tel and not tel.isdigit():
            raise serializers.ValidationError({"detail": ["Telefonnummer darf nur Zahlen enthalten."]})

        if CustomUser.objects.filter(tel=tel).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"detail": ["Diese Telefonnummer ist bereits vergeben."]})

        return tel

class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

    def get_user(self, obj):
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
        return {
            "pk": obj.id,
            "username": obj.username,
            "first_name": obj.first_name or "",
            "last_name": obj.last_name or ""
        }
