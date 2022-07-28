import os
from datetime import datetime
from app.models import *
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from rest_framework.authtoken.models import Token
from channels.auth import AuthMiddlewareStack
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth.models import User
from django.db import close_old_connections

ALGORITHM = "HS256"

@database_sync_to_async
def get_user(token):
    try:
        payload = Token.objects.get(key=token)
        print('payload', payload.user)
    except:
        print('no payload')
        return AnonymousUser()

    return payload.user
@database_sync_to_async
def get_device(key):
    try:
        payload = Device.objects.get(key=key)
        print('payload', payload)
    except:
        print('no payload')
        return None


    return payload


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        print(scope)
        # token_key = scope['query_string'].decode().split('=')[-1]
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    scope['user'] = await get_user(token_key)
                    print('d2', scope['user'])
                    return await super().__call__(scope, receive, send)
                elif token_name == 'Key':
                    scope['key'] = await get_device(token_key)
                    print('d2', scope['key'])
                    return await super().__call__(scope, receive, send)
            except ValueError:
                token_key = None
                print("Token Key:", token_key)
        else: 
            try:
                token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
                scope['user'] = await get_user(token_key)
                print('d2', scope['user'])
                return await super().__call__(scope, receive, send)
            except ValueError:
                token_key = None
        # try:
        #     token_key = dict(scope['headers'])[b'sec-websocket-protocol'].decode('utf-8')
        #     print('d1', token_key)
        # except ValueError:
        #     token_key = None

        


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)