from __future__ import absolute_import
from celery import shared_task
from day01.celery import async_task

import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from webchat import settings
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


# @shared_task
@async_task.task
def tailf(id, channel_name):
    channel_layer = get_channel_layer()
    filename = settings.TAILF[int(id)]

    try:
        with open(filename) as f:
            f.seek(0, 2)

            while True:
                """
                注：tasks硬性时间规定，300s，判定任务超时失败，task任务被强制终止，websocket链接存在但是无法再监控文件内容，仅能断开链接重新发送
                [2020-09-02 11:54:00,646: ERROR/MainProcess] Task handler raised error: TimeLimitExceeded(300.0)
                Traceback (most recent call last):
                  File "/home/workon/env/envbuild/ddjango/lib/python3.7/site-packages/billiard/pool.py", line 684, in on_hard_timeout
                    raise TimeLimitExceeded(job._timeout)
                billiard.exceptions.TimeLimitExceeded: TimeLimitExceeded(300.0,)
                [2020-09-02 11:54:00,647: ERROR/MainProcess] Hard time limit (300.0s) exceeded for webchat.tasks.tailf[15433031-d8f3-4dff-a7a2-2e712c0ca1cf]
                [2020-09-02 11:54:00,752: ERROR/MainProcess] Process 'ForkPoolWorker-10' pid:12964 exited with 'signal 9 (SIGKILL)'
                """
                line = f.readline()
                if line:
                    logger.info('监听中: {0} + {1}'.format(channel_name, line))
                    async_to_sync(channel_layer.send)(
                        channel_name,
                        {
                            "type": "send.message",
                            "message": "微信公众号【运维咖啡吧】原创 版权所有 " + str(line)
                        }
                    )
                    # # 发送到组
                    # async_to_sync(channel_layer.group_send)(
                    #     group_name,
                    #     {
                    #         'type': 'chat.message',
                    #         'message': '欢迎关注公众号【运维咖啡吧】'
                    #     }
                    # )
                else:
                    time.sleep(0.2)
    except Exception as e:
        print(e)
