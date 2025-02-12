from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        """
        Determine if the request has permission.

        Permissions are granted based on the request method:
        - "POST": Allows access if the request user is a customer user.
        - All other methods: Allows access.
        """
        
        if request.method == "POST":
            return hasattr(request.user, "type") and request.user.type == "customer"
        return True

class IsOwnerOrderOrOffer(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        """
        Determine if the request has object-level permission.
    
        Permissions are granted based on the request method:
        - "GET": Allows access if the request user is either the customer or business user associated with the object.
        - "PATCH": Allows access if the request user is the business user associated with the object.
        - "DELETE": Allows access if the request user is a staff member.
    
        Returns True if the request method is not one of the specified types.
        """

        if request.method == "GET":
            return obj.customer_user == request.user or obj.business_user == request.user

        if request.method == "PATCH":
            return obj.business_user == request.user

        if request.method == "DELETE":
            return request.user.is_staff

        return True