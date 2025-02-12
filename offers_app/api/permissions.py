from rest_framework.permissions import BasePermission

class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        """
        Determine if the request has permission to access the view.

        Permissions are granted based on the request method:
        - "POST": Allows access if the request user is a business user.
        - All other methods: Allow access.

        Returns True if the request method is not one of the specified types.
        """
        
        if request.method == "POST":
            return hasattr(request.user, "type") and request.user.type == "business"
        return True