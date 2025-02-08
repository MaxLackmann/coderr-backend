from rest_framework.permissions import BasePermission

class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return hasattr(request.user, "type") and request.user.type == "business"
        return True