from django.test import TestCase
import threading
# Create your tests here.


# class Singleton:
#
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         print("New")
#         if cls._instance is None:
#             print("Create")
#             cls._instance = super().__new__(cls, *args, **kwargs)
#         return cls._instance
#
#     def __init__(self):
#         print("Initialize")
#         self.prop = None
#
#
# s1 = Singleton()
# s2 = Singleton()

# # 线程安全单例模式
#
#
# class Singleton(object):
#     _instance_lock = threading.Lock()
#
#     def __init__(self, num):
#         self.num = num
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Singleton, "_instance"):
#             with cls._instance_lock:
#                 # 二次检查防止获取锁过程中已经被改变属性
#                 if not hasattr(Singleton, "_instance"):
#                     cls._instance = object.__new__(cls)
#         return cls._instance
#
#
# def task(*arg):
#     obj = Singleton(arg[0])
#     print(obj)
#
#
# for i in range(5):
#     t = threading.Thread(target=task, args=[i, ])
#     t.start()
#
#
# # 上下文管理器
# class Context():
#     def __init__(self):
#         print("初始化")
#
#     def __enter__(self):
#         print("开始执行...")
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("结束了")
#
#     def operate(self):
#         print('===in operation===')
#
#
# with Context() as ctx:
#     ctx.operate()

# class logger(object):
#     def __init__(self, level='INFO'):
#         self.level = level
#
#     def __call__(self, func): # 接受函数
#         def wrapper(*args, **kwargs):
#             print("[{level}]: the function {func}() is running..."\
#                 .format(level=self.level, func=func.__name__))
#             func(*args, **kwargs)
#         return wrapper  #返回函数
#
# @logger(level='WARNING')
# def say(something):
#     print("say {}!".format(something))
#
# say("hello")

import time
import functools


class DelayFunc:
    def __init__(self, duration, func):
        self.duration = duration
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f'Wait for {self.duration} seconds...')
        time.sleep(self.duration)
        return self.func(*args, **kwargs)

    def eager_call(self, *args, **kwargs):
        print('Call without delay')
        return self.func(*args, **kwargs)


def delay(duration):
    """
    装饰器：推迟某个函数的执行。
    同时提供 .eager_call 方法立即执行
    """
    # 此处为了避免定义额外函数，
    # 直接使用 functools.partial 帮助构造 DelayFunc 实例
    return functools.partial(DelayFunc, duration)


@delay(duration=2)
def add(a, b):
    return a + b


add(3, 5)
