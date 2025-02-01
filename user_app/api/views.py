from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny
from .authentication import CombinedTokenAuthentication
from .permissions import IsAuthenticatedOrGuest
from user_app.api.services import UserService
from user_app.models import CustomUser

class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = UserService.register_user(serializer.validated_data)
            token = UserService.generate_token(user)
            return Response({"token": token, "username": user.username, "email": user.email, "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.update_activity()
            token = UserService.generate_token(user)
            return Response({"token": token, "username": user.username, "email": user.email, "user_id": user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request, user_id):
        user = UserService.get_profile(user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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