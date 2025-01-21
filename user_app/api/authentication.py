from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user_app.models import GuestToken
from django.utils.timezone import now

class GuestTokenAuthentication(TokenAuthentication):
    """Erlaubt die Authentifizierung über GuestTokens"""
    model = GuestToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed("Invalid guest token")

        if token.is_expired():
            token.delete()
            raise AuthenticationFailed("Guest token expired")

        return (token.user, token)