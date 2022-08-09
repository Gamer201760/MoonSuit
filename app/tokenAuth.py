from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
import os
from app.models import *
from api.models import User
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


ALGORITHM = "HS256"


@database_sync_to_async
def _getUser(token: str) -> User:
    try:
        return Token.objects.get(key=token).user
    except:
        return None


@database_sync_to_async
def _getDevice(user: User, key: str) -> Device:
    try:
        return Device.objects.get(owner=user, key=key)
    except:
        return None


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        headers = dict(scope['headers'])
        query_string = scope.get("query_string")
        query_string = query_string.decode("utf-8")

        query_string = query_string.split("=")

        if query_string[0] == "token":
            token_key = query_string[-1]
        
            user = await _getUser(token_key)

            if user is not None:
                scope["user"] = user
                scope["user_token"] = token_key
                return await super().__call__(scope, receive, send)

        if b'authorization' in headers and b"key" in headers:
            _token, token = headers[b"authorization"].strip().split()
            _key, key = headers[b"key"].strip().split()

            key = key.decode("utf-8")
            token = token.decode("utf-8")

            user = await _getUser(token)
            device = await _getDevice(user, key)

            if device is not None and user is not None:
                scope["device"] = device
                scope["user"] = user
                scope["user_token"] = token

                return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
