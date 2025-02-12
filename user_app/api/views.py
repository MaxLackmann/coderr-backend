from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from rest_framework.permissions import AllowAny
from .authentication import CombinedTokenAuthentication
from .permissions import IsAuthenticatedOrGuest
from user_app.api.services import UserService
from user_app.models import CustomUser

class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles the POST request to the registration endpoint.

        Creates a new user account and generates a token for the user.

        Args:
            request (Request): The request object containing the registration data.

        Returns:
            Response: A response object containing the new user's data and a token.
        """
        
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserService.register_user(serializer.validated_data)
        token = UserService.generate_token(user)
        return Response(
            {
                "token": token,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles the POST request to the login endpoint.

        Authenticates the user using the provided data and returns a token if successful.

        Args:
            request (Request): The request object containing the login data.

        Returns:
            Response: A response object containing the user's data and a token if the login is successful.
        """

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
        return Response(
            {
                "token": token,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            },
            status=status.HTTP_200_OK
        )

class ProfileView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request, pk):
        """
        Retrieves a user profile by its primary key.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the user to retrieve.

        Returns:
            Response: A response object containing the user's data if the retrieval is successful.
        """

        try:
            user = UserService.get_profile(pk)
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": ["Benutzer wurde nicht gefunden."]}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        """
        Partially updates a user profile by its primary key.
    
        Args:
            request (Request): The request object containing the update data.
            pk (int): The primary key of the user to update.
    
        Returns:
            Response: A response object containing the updated user's data if the update is successful.
    
        Raises:
            403 Forbidden: If the requesting user is not authorized to update the profile.
            404 Not Found: If the user does not exist.
            400 Bad Request: If the request data is invalid.
        """

        try:
            user = UserService.get_profile(pk)

            if request.user != user and not request.user.is_staff:
                return Response({"detail": ["Nicht autorisiert."]}, status=status.HTTP_403_FORBIDDEN)

            serializer = ProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"detail": ["Benutzer wurde nicht gefunden."]}, status=status.HTTP_404_NOT_FOUND)

class BusinessProfilesView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request):
        """
        Retrieves a list of business users.

        Returns:
            Response: A response object containing a list of business users' data if the retrieval is successful.
        """

        business_users = CustomUser.objects.filter(type='business')
        serializer = BusinessProfileSerializer(business_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerProfilesView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request):
        """
        Retrieves a list of customer users.

        Returns:
            Response: A response object containing a list of customer users' data if the retrieval is successful.
        """

        customer_users = CustomUser.objects.filter(type='customer')
        serializer = CustomerProfileSerializer(customer_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
