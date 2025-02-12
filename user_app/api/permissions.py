from rest_framework.permissions import BasePermission
from user_app.models import GuestToken

class IsAuthenticatedOrGuest(BasePermission):
    def has_permission(self, request, view):
        """
        Determines if the request has permission to access the view.

        Permissions are granted based on the following criteria:
        - Allows access if the request user is authenticated and a staff member.
        - Allows access if the request user is authenticated.
        - Allows access if the request has a valid GuestToken.

        Returns True if any of the conditions are met, otherwise False.
        """
        
        if request.user.is_authenticated and request.user.is_staff:
            return True

        if request.user.is_authenticated:
            return True

        guest_token = request.auth
        return isinstance(guest_token, GuestToken)