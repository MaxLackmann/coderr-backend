from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny
from .authentication import CombinedTokenAuthentication
from .permissions import IsAuthenticatedOrGuest
from user_app.api.services import UserService
from user_app.models import CustomUser
from django.db import IntegrityError

class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": ["Ungültige Daten. Bitte überprüfe deine Eingabe."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserService.register_user(serializer.validated_data)
            token = UserService.generate_token(user)
            return Response({"token": token, "username": user.username, "email": user.email, "user_id": user.id}, status=status.HTTP_201_CREATED)
        
        except IntegrityError as e:
            if 'email' in str(e):
                return Response({"detail": ["E-Mail existiert bereits."]}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in str(e):
                return Response({"detail": ["Username existiert bereits."]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": ["Registrierung fehlgeschlagen."]}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": ["Ungültige Eingabe. Bitte überprüfe deine Daten."]}, status=status.HTTP_400_BAD_REQUEST)

        user = UserService.authenticate_user(
            serializer.validated_data["username"],
            serializer.validated_data["password"]
        )

        if user is None:
            return Response({"detail": ["Username oder Passwort nicht korrekt."]}, status=status.HTTP_400_BAD_REQUEST)

        user.update_activity()
        token = UserService.generate_token(user)
        return Response({"token": token, "username": user.username, "email": user.email, "user_id": user.id}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request, user_id):
        try:
            user = UserService.get_profile(user_id)
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": ["Benutzer wurde nicht gefunden."]}, status=status.HTTP_404_NOT_FOUND)

class BusinessProfilesView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request):
        business_users = CustomUser.objects.filter(type='business')
        serializer = ProfileSerializer(business_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomerProfilesView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request):
        customer_users = UserService.get_filtered_profiles("customer")
        serializer = ProfileSerializer(customer_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)