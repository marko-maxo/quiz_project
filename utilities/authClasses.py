from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from .tokenFunctions import decodeJWT


class JWTCustomAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_cookie = False
        try:
            jwt_cookie = request.COOKIES["jwt"]
        except:
            raise exceptions.AuthenticationFailed("JWT is not valid")

        if not jwt_cookie:
            raise exceptions.AuthenticationFailed("JWT not valid")

        decoded = decodeJWT(jwt_cookie)
        if decoded[0]:
            return User.objects.get(id=decoded[1]["id"]), None
        else:
            raise exceptions.AuthenticationFailed("Invalid JWT")
