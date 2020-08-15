from app01.models import UserProfile, UserLog
from app01.hand import Hand
from day01.celery import async_task
import asyncio, random


@async_task.task
def select(num):
    example = UserProfile.objects.get(pk=num)
    print("查询成功，返回结果 %s" % example.username)
    name = str(example.username)
    # asyncio.sleep(random.random())
    return name
    # 为一个数据对象增加了新的属性
    # new_hand = Hand(*hand)
    # example.hand = new_hand
    # # print(example.hand.north)   # 数据访问方式，仅在本次请求中可以对新增对属性进行存取
    #
    # example.save()
    # return example.hand.north


@async_task.task
def event_log(name, info):
    """
    用户操作日志记录
    :param user:
    :param log_type:
    :param event_type:
    :param detail:
    :param address:
    :param useragent:
    :param other_info:
    :return:
    """
    UserLog.objects.create(
        name=name,
        info=info
    )


@async_task.task
def my_task1(a, b):
    asyncio.sleep(random.random())
    print("任务函数(my_task1)正在执行....")
    return a + b


@async_task.task
def my_task2(a, b):
    print("任务函数(my_task2)正在执行....")
    return a + b


@async_task.task
def my_task3(a, b):
    print("任务函数(my_task3)正在执行....")
    return a + b
