from rest_framework.permissions import BasePermission
from user_app.models import GuestToken

class IsAuthenticatedOrGuest(BasePermission):
    def has_permission(self, request, view):
        """
        Determines if the request has permission to access the view.

        Permissions are granted based on the request method and the user's authentication status:

        - Allows access if the request method is "GET".
        - Allows access if the request user is an authenticated staff user.
        - Allows access if the request user is an authenticated user.
        - Allows access if the request user is an authenticated guest user.

        Returns False if none of the conditions are met.
        """

        if request.method == "GET":
            return True
        
        if request.user.is_authenticated and request.user.is_staff:
            return True

        if request.user.is_authenticated:
            return True

        guest_token = request.auth
        return isinstance(guest_token, GuestToken)