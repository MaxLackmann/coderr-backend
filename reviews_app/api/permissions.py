from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class CanModifyReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.user == obj.reviewer:
            return True

        return False
    
class CanCreateReview(BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        if request.user.type != "customer":
            raise PermissionDenied({"detail": ["Nur Kunden dürfen Bewertungen abgeben."]})

        return True