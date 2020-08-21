from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from app01.models import UserLog
# 自定义信号量
from app02.my_signals import pizza_done
# 异步包装
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async

"""信号量无法使用异步视图"""
def test(request):
    UserLog.objects.create(
        name="app01",
        info="测试信号量"
    )
    print("执行完毕")
    return HttpResponse("test")


def test_signal(request):
    # 模型信号量测试
    UserLog.objects.create(
        name="app01",
        info="测试信号量"
    )
    print("执行完毕")

    # 自定义信号量测试 自定义文件/内容任意可访问位置
    pizza_done.send(sender='seven', toppings=123, size=456)

    return JsonResponse({'code': 200, "status": "成功"})
