from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class CanModifyReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Determines if the request has object-level permission to modify a review.
    
        Permissions are granted based on the following criteria:
        - Allows access if the request user is a staff member.
        - Allows access if the request user is the reviewer associated with the object.
    
        Returns False if none of the conditions are met.
        """

        if request.user.is_staff:
            return True

        if request.user == obj.reviewer:
            return True

        return False
    
class CanCreateReview(BasePermission):
    def has_permission(self, request, view):
        """
        Determines if the request has permission to create a review.
    
        Permissions are granted based on the following criteria:
        - Allows access if the request method is not "POST".
        - Allows access if the request user is a customer.
    
        Raises a 403 Forbidden error if the user is not a customer.
    
        Returns True if the permission is granted, otherwise False.
        """
        
        if request.method != "POST":
            return True

        if request.user.type != "customer":
            raise PermissionDenied({"detail": ["Nur Kunden dürfen Bewertungen abgeben."]})

        return True