# PS: django的signal是同步的
# 如果把信号量处理写在项目根目录内的__init__则是全局
# 内置信号量 https://docs.djangoproject.com/en/3.1/ref/signals/
from django.db.models.signals import pre_save, post_save


def pre_save_func(sender, **kwargs):
    print("pre_save_func")
    print("pre_save_msg:", sender, kwargs)


pre_save.connect(pre_save_func)  # models对象保存前触发callback函数
pre_save.disconnect()  # 关闭信号


def post_save_func(sender, **kwargs):
    print("post_save_func")
    print("post_save_msg:", sender, kwargs)


post_save.connect(post_save_func)  # models对象保存后触发函数
post_save.disconnect()

# 装饰器触发函数
# from django.core.signals import request_finished
# from django.dispatch import receiver
# from app.views import xxx
#
# @receiver(request_finished, sender=app02Test)
# def callback(sender, **kwargs):
#     print("Request finished!")
