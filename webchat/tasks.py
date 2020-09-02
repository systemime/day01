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
                    time.sleep(0.5)
    except Exception as e:
        print(e)
