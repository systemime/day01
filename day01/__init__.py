from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import async_task as celery_app

__all__ = ('celery_app',)  # 自动加载所有使用celery装饰器的视图
