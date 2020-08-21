# django-celery已弃用 4.0以后的celery版本已经不区分celery和django-celery
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms
from django.conf import settings

from datetime import timedelta
from celery.schedules import crontab

# 把置默认的django settings模块配置给celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day01.settings.base')
async_task = Celery('day01')

# 这里使用字符串以使celery的worker不用为子进程序列化配置对象。
async_task.config_from_object('django.conf:settings', namespace='CELERY')

# # 自动加载每个应用(app)目录下的tasks.py文件
async_task.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# async_task.autodiscover_tasks()

# Allow root user run celery
platforms.C_FORCE_ROOT = True


@async_task.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# # 定期任务
# # 参考 https://mp.weixin.qq.com/s/lXrp3igYo9W2UuE5Gauysg
# async_task.conf.update(
#     CELERYBEAT_SCHEDULE={
#         'kill-except': {  # 别名
#             'task': 'selectos.tasks.regular_kill',  # task任务所在位置
#             'schedule':  timedelta(minutes=5),
#             # 'schedule': crontab(hour=4, minute=30, day_of_week=1),  # crontab任务计划
#             # 'args': (xxx, xxx),  # 传入参数  # 函数参数
#             'options': {
#                 'queue': 'regular_queue',
#             }
#         },
#         'monitor_plan': {
#             'task': 'component.tasks.task_monitor',
#             'schedule': crontab(hour=4, minute=30, day_of_week=1),
#             'options': {
#                 'queue': 'regular_queue',
#             }
#         },
#     }
# )

# delay()方法执行，此时会将任务委托给celery后台的worker执行
# 由于使用了RabbitMQ 创建了消息队列，每次发生修改必须重新启动celery任务，否则设置队列无效

# @app.task使用
# 在setting中如果设置了对应路由，@app.task无需指定name='queue_name'参数，若未指定则需要

# 定时请不要使用绝对时间
# 来自GitHub的解释 https://github.com/celery/django-celery-beat
# 如果更改Django TIME_ZONE设置，则定期任务计划仍将基于旧时区。
# 要解决此问题，您必须为每个定期任务重置“上次运行时间”：
# 请注意，这将重置状态，就好像以前从未执行过定期任务一样。
