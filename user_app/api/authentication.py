from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from user_app.models import GuestToken
from django.utils.timezone import now

class CombinedTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        token_key = self.get_token_from_request(request)
        if not token_key:
            raise AuthenticationFailed({"token": "No authentication token provided"})

        guest_auth = self.authenticate_guest_token(token_key)
        if guest_auth is not None:
            return guest_auth
        
        auth = super().authenticate(request)
        if auth is not None:
            return auth

        raise AuthenticationFailed({"token": "Invalid or expired token"})

    def get_token_from_request(self, request):
        auth = request.headers.get("Authorization", "").split()
        if len(auth) == 2 and auth[0].lower() == "token":
            return auth[1]
        return None

    def authenticate_guest_token(self, key):
        try:
            token = GuestToken.objects.get(key=key)
        except GuestToken.DoesNotExist:
            return None

        if token.is_expired():
            token.delete()
            raise AuthenticationFailed({"token": "Guest token expired"})

        return (token.user, token)