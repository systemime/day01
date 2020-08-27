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
import importlib

from django.core.handlers.asgi import ASGIHandler
from channels import routing


def get_asgi_application():
    """
    重载方法，支持websocket
    """
    django.setup(set_prefix=False)
    # return RefactorASGIHandlerOne()
    return RefactorASGIHandlerTwo()


class RefactorASGIHandlerTwo(ASGIHandler):
    """
    - 自建Websocket类功能不够完善
    - 尝试使用django-channles直接增强asgi功能
      - 主要测试：异步支持及稳定性
    """
    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            return routing.get_default_application()

        await super().__call__(scope, receive, send)


class RefactorASGIHandlerOne(ASGIHandler):
    """20/8/25
    关键问题在于，对请求类型对判断
    websocket链接的协议是websocket，ws需要指定端口进行，wss链接可以使用域名配合证书实现任务
    gunicorn或者其他部署方式，使用unix socket配合nginx是比较好的方案，但是ws无法指定端口，任务被识别为http
    另外，自己重载websocket的class仅仅支持基本的链接，无法分组等任务

    django3.1及以前，websocket仍然推荐使用django-channle实现
    注：不支持django3(asgi)版本，未找到兼容方案
    django3.2及以后版本，后续发布再测试
    """
    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            match = resolve(scope["raw_path"])
            await match.func(WebSocket(scope, receive, send), *match.args, **match.kwargs)
            return

        await super().__call__(scope, receive, send)
