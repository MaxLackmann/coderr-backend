from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user_app.models import GuestToken

class CombinedTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        """
        Authenticates a request using the provided token.

        If the request method is GET, returns None without attempting authentication.
        If the token is invalid or expired, raises AuthenticationFailed with an appropriate error message.
        Otherwise, returns a tuple of (user, auth_token) if authentication is successful.

        :param request: The request to authenticate.
        :return: A tuple of (user, auth_token) if authentication is successful, None if the request method is GET.
        :raises: AuthenticationFailed if the token is invalid or expired.
        """

        if request.method == "GET":
            return None

        token_key = self.get_token_from_request(request)
        if not token_key:
            raise AuthenticationFailed({"token": "No authentication token provided"})

        guest_auth = self.authenticate_guest_token(token_key)
        if guest_auth is not None:
            return guest_auth
        
        auth = super().authenticate(request)
        if auth is not None:
            return auth
        
        token = request.headers.get("auth-token")
        if not token:
            return None

        raise AuthenticationFailed({"token": "Invalid or expired token"})

    def get_token_from_request(self, request):
        """
        Extract the token from the given request object.

        :param request: The request object to extract the token from.
        :return: The extracted token if it exists, None if not.
        """

        auth = request.headers.get("Authorization", "").split()
        if len(auth) == 2 and auth[0].lower() == "token":
            return auth[1]
        return None

    def authenticate_guest_token(self, key):
        """
        Authenticates a user using a guest token key.

        Attempts to retrieve a `GuestToken` object using the provided key. If the token
        exists and is not expired, returns a tuple of the associated user and the token.
        If the token does not exist or is expired, handles the exception or raises an
        authentication failure, respectively.

        :param key: The guest token key used for authentication.
        :return: A tuple of the user and guest token if successful, or None if the token does not exist.
        :raises: AuthenticationFailed if the token is expired.
        """

        try:
            token = GuestToken.objects.get(key=key)
        except GuestToken.DoesNotExist:
            return None

        if token.is_expired():
            token.delete()
            raise AuthenticationFailed({"token": "Guest token expired"})

        return (token.user, token)