import jwt
from django.conf import settings
import time

jwt_secret = settings.JWT_SECRET


def createJWT(user):
    now = time.time()
    return jwt.encode(
        {"username": user.username, "id": user.id, "iat": now, "exp": now + 86400},
        jwt_secret,
        algorithm="HS256")


def decodeJWT(token):
    try:
        decoded = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except:
        return False, "Secret is not valid"

    if decoded["exp"] < time.time():
        return False, "Token has expired"

    return True, decoded
