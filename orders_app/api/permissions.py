from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return hasattr(request.user, "type") and request.user.type == "customer"
        return True

class IsOwnerOrderOrOffer(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return obj.customer_user == request.user or obj.business_user == request.user

        if request.method == "PATCH":
            return obj.customer_user == request.user

        if request.method == "DELETE":
            return request.user.is_staff

        return True