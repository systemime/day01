# -*- coding: utf-8 -*-
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # 使用django自带auth认证获取信息
from channels.sessions import SessionMiddlewareStack  # 从session中获取信息
from webchat.routing import websocket_urlpatterns
from webchat.utils.tools import TokenAuthMiddlewareStack  # 包装了session和auth

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(  # 选择中间件
        URLRouter(
            # re_path(r'^pod/(?P<name>\w+)', SSHConsumer),
            # A + B + C + ...  # 导入app中websocket路由
            websocket_urlpatterns  # 导入app中websocket路由
        )
    ),
})

