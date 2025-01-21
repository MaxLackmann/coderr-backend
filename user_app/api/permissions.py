from rest_framework.permissions import BasePermission
from user_app.models import GuestToken

class IsAuthenticatedOrGuest(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        guest_token = request.auth
        return isinstance(guest_token, GuestToken)