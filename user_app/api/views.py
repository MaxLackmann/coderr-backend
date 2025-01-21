from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from ..models import CustomUser, GuestToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .authentication import GuestTokenAuthentication
from .permissions import IsAuthenticatedOrGuest
from django.utils.crypto import get_random_string

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            user.update_activity()

            if user.username in ["andrey", "kevin"]:  
                token = GuestToken.objects.create(user=user, key=get_random_string(40))
            else:
                token, _ = Token.objects.get_or_create(user=user)

            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }
            print(user.type, token.key)
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    authentication_classes = [GuestTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BusinessProfilesView(APIView):
    authentication_classes = [GuestTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request):
        business_users = CustomUser.objects.filter(type='business')
        serializer = ProfileSerializer(business_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerProfilesView(APIView):
    authentication_classes = [GuestTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request):
        customer_users = CustomUser.objects.filter(type='customer')
        serializer = ProfileSerializer(customer_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)