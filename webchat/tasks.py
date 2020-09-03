from __future__ import absolute_import
from celery import shared_task
from day01.celery import async_task

import time
import asyncio
import paramiko
import select

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
                注：tasks有硬性时间规定，一般为300s判定任务超时失败，task任务被强制终止，可以自定义配置
                   如果task任务超时中断，websocket链接存在但是无法再监控文件内容，仅能断开链接重新发送
                示例：
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
                            "message": "当前输出内容:  " + str(line)
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
                    asyncio.sleep(0.2)
    except Exception as e:
        print(e)


@async_task.task
def tailf_tail(id, channel_name):
    """
    重写使用paramiko与系统交互，通过tail命令监控文件
    手动清理用户：
            w
            pkill -kill -t pts/6
            ps -ef | grep pts/6
            kill -9 xxx
    :param id:
    :param channel_name:
    :return:
    """
    channel_layer = get_channel_layer()
    filename = settings.TAILF[int(id)]

    # 进行连接
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('127.0.0.1', 22, username='workon', password='547520feng', timeout=4)
    # 开启channel 管道
    transport = client.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    tail = 'tail -f %s' % filename
    # 将命令传入管道中
    channel.exec_command(tail)

    while True:
        # 判断退出的准备状态
        if channel.exit_status_ready():
            break
        try:
            # 通过socket进行读取日志，linux相当于客户端，我本地相当于服务端请求获取数据
            rl, wl, el = select.select([channel], [], [])
            if len(rl) > 0:
                recv = channel.recv(10240)
                # 此处将获取的数据解码成gbk发送
                print(recv.decode('utf-8', 'ignore'))
                async_to_sync(channel_layer.send)(
                    channel_name,
                    {
                        "type": "send.message",
                        "message": "当前输出内容:  " + str(recv.decode('utf-8', 'ignore'))
                    }
                )
        # 键盘终端异常
        except KeyboardInterrupt:
            channel.send("\x03")  # 发送 ctrl+c
            channel.close()
    client.close()

