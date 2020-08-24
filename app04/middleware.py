from django.urls import resolve
from .connection import WebSocket


def websockets(app):
    async def asgi(scope, receive, send):
        if scope["type"] == "websocket":
            match = resolve(scope["raw_path"])
            await match.func(WebSocket(scope, receive, send), *match.args, **match.kwargs)
            return
        await app(scope, receive, send)

    return asgi


import django
from django.core.handlers.asgi import ASGIHandler


def get_asgi_application():
    """
    重载方法，支持websocket
    """
    django.setup(set_prefix=False)
    return RefactorASGIHandler()


class RefactorASGIHandler(ASGIHandler):

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            match = resolve(scope["raw_path"])
            await match.func(WebSocket(scope, receive, send), *match.args, **match.kwargs)
            return

        await super().__call__(scope, receive, send)
