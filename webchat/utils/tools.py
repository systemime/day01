from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(headers):
    try:
        token_name, token_key = headers[b'authorization'].decode().split()
        if token_name == 'Token':
            token = Token.objects.get(key=token_key)
            return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    """
    Yeah, this is black magic:
    https://github.com/django/channels/issues/1399
    """
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            self.scope['user'] = await get_user(headers)
        inner = self.inner(self.scope)
        return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
#
# from channels.db import database_sync_to_async
#
# @database_sync_to_async
# def get_user(user_id):
#     try:
#         return User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return AnonymousUser()
#
# class QueryAuthMiddleware:
#     """
#     Custom middleware (insecure) that takes user IDs from the query string.
#     """
#
#     def __init__(self, inner):
#         # Store the ASGI application we were passed
#         self.inner = inner
#
#     def __call__(self, scope):
#         return QueryAuthMiddlewareInstance(scope, self)
#
#
# class QueryAuthMiddlewareInstance:
#     def __init__(self, scope, middleware):
#         self.middleware = middleware
#         self.scope = dict(scope)
#         self.inner = self.middleware.inner
#
#     async def __call__(self, receive, send):
#         self.scope['user'] = await get_user(int(self.scope["query_string"]))
#         inner = self.inner(self.scope)
#         return await inner(receive, send)
#
# TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
