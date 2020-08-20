# 定义信号
# django应该使用celery的异步任务信号量
import django.dispatch
from asgiref.sync import sync_to_async

pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])


# 注册信号
def callback(sender, **kwargs):
    print("callback")
    print(sender, kwargs)


pizza_done.connect(callback)
pizza_done.disconnect()

# 使用装饰器
# from django.dispatch import receiver
# @receiver(pizza_done, sender=callback)
# def my_callback(sender, **kwargs):
#     print("我在%s时间收到来自%s的信号，请求url为%s" % (kwargs['time'], sender, kwargs["path"]))
