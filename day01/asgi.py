"""
ASGI config for day01 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

# from django.core.asgi import get_asgi_application
from app04.middleware import get_asgi_application
from app04.middleware import websockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day01.settings.base')

application = get_asgi_application()

# 1. 修改/home/workon/env/envbuild/ddjango/lib/python3.7/site-packages/django/core/handlers/asgi.py源码
# 可以起到同样的效果,
# 2. 对application进行包装
# application = websockets(application)
# 3. 重载get_asgi_application方法
# 创建子类
