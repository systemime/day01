# -*- coding: utf-8 -*-
"""
routing功能类似django中url路由功能
"""
from django.urls import re_path, path
from webchat.consumers import ChatConsumer

websocket_urlpatterns = [
    # re_path(r'^pod/(?P<name>[\w-]+)/(?P<namespace>\w+)/(?P<cols>\d+)/(?P<rows>\d+)$', SSHConsumer),  # name获取
    path('ws/chat/', ChatConsumer),
]
