from django.views.generic import View
# from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# 请求限制器
from django.views.decorators.http import require_http_methods
# 类装饰器
from django.utils.decorators import method_decorator
# Gzip
# 缓存模块
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# 私有缓存控制 1
from django.views.decorators.cache import cache_control
# 私有缓存控制 2
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import patch_cache_control
# 邮件操作
# 日志控制
import logging


from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from aiohttp import ClientSession

# 模型
from app01.models import UserProfile
from app01.hand import Hand
from day01.celery import async_task
from app01.tasks import select, event_log, my_task1, my_task2, my_task3
from celery import group, signature

import requests
import random
import asyncio
import aiohttp
import datetime
import types


async def test(request):
    # t1 = signature(my_task1, args=(1, 2))
    # t2 = signature(my_task2, args=(1, 2))
    # t3 = signature(my_task3, args=(1, 2))
    # t4 = signature(select, args=(1, ))
    # my_group = group(t1, t2, t3, t4).apply_async(queue='select_queue')
    # res = my_group.get()

    t4 = select.apply_async((1,))
    res = sync_to_async(t4.get)

    # ret = select.apply_async((1, ["north", "east", "south", "west"]), queue='select_queue', countdown=1)
    # res = async_task.AsyncResult(ret)
    # print(res.status)
    return HttpResponse(res)


# @method_decorator(gzip_page, name='dispatch')  # 装饰整个类
class Index(View):

    # 私有缓存控制 1，请求方法限制，缓存并缓存时间
    get_decorators = [cache_control(private=True), require_http_methods(['GET', ]), cache_page(60 * 15)]

    # @method_decorator(patch_cache_control())
    @method_decorator(get_decorators)
    def get(self, request):
        name = cache.get('my_key')
        # cache.get_many(['a', 'b', 'c'])
        # cache.delete('xxx')
        # cache.delete_many(['a', 'b', 'c'])
        # cache.clear()
        # # 重新设置过期时间
        cache.touch('my_key', 60 * 15)
        # # 缓存增 1
        # cache.incr(key, delta=1, version=None)
        # # 缓存减 1
        # cache.decr(key, delta=1, version=None)

        logger = logging.getLogger(__name__)
        logger.info('Something went send!')

        context = {
            "key": "asdfo23jhj45k2l",
            "msg": "你好",
            "name": name
        }
        return render(request, "index.html", context)

    @method_decorator(vary_on_cookie)  # 私有缓存控制 2
    @method_decorator(cache_page(60 * 15))
    @method_decorator(require_http_methods(['POST']))
    def post(self, request):
        response = HttpResponse()
        name = cache.get('my_key')
        response.write("<h2>{name}</h2>".format(name=name))
        patch_cache_control(response, private=True)  # 私有缓存控制 2

        return response


# @ example
async def current_datetime(request):
    now = datetime.datetime.now()
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.baidu.com') as resp:
            data = await resp.read()  # 已知bug，resp.text()会导致无限刷新

    name = await Testasync.get_username()
    cache.get_or_set('my_key', name, 60 * 15)
    cache.set_many({'a': 1, 'b': 2, 'c': 3})

    html = '<html><body>It is now %s.<br>HTML: %s<br> %s</body></html>' % (now, data, name)
    return HttpResponse(html)


class Testasync(View):

    @staticmethod
    @sync_to_async
    def get_username():
        user = UserProfile.objects.first()
        return user.username

    async def current_datetime(self, request):
        now = datetime.datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.baidu.com') as resp:
                data = await resp.read()

        username = await self.get_username()
        html = f"<html>" \
               f"<body>Hey, {username}, it is now {now}. " \
               f"Here's your random cat fact: {data.decode('utf-8')}</body>" \
               f"</html>"
        return html

    def get(self, request):
        result = async_to_sync(self.current_datetime, force_new_loop=True)(request)
        return JsonResponse({"result": result})


class Testsync(View):
    def get_username(self):
        user = UserProfile.objects.last()
        return user.username

    def current_datetime(self, request):
        now = datetime.datetime.now()
        data = requests.get("https://www.baidu.com").text

        username = self.get_username()
        html = f"<html><body>Hey, {username}, it is now {now}. " \
               f"Here's your random cat fact: {data}</body></html>"
        return html

    def get(self, request):
        result = self.current_datetime(request)
        # await send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'cchandler@qq.com',
        #     ['1767474418@qq.com'],
        #     fail_silently=False,
        # )
        # datatuple = (
        #     ('Subject', 'Message.', 'cchandler@qq.com', ['1767474418@qq.com']),
        #     ('Subject', 'Message.', 'cchandler@qq.com', ['547feng@163.com']),
        # )
        # await send_mass_mail(datatuple)
        # with mail.get_connection() as connection:
        #     mail.EmailMessage(
        #         'subject1', 'body1', 'cchandler', ['1767474418@qq.com'],
        #         connection=connection,
        #     ).send()
        #     mail.EmailMessage(
        #         'subject2', 'body2', 'cchandler', ['547feng@163.com'],
        #         connection=connection,
        #     ).send()
        return JsonResponse(result, safe=False)


class TornAsyncioView(View):
    def get(self, request, *args, **kwargs):
        # reslure = async_to_sync(self.my_view)(request)
        reslure = async_to_sync(self.request_status)
        print(reslure)
        return JsonResponse({"reslure": reslure()})

    async def request_status(self):
        url = "http://geekae.top"
        async with ClientSession() as session:
            async with session.get(url) as response:
                response = await response.read()
                response = response.decode("utf-8")
                return response

    async def my_view(self, request):
        await asyncio.sleep(random.random())
        return 'Hello, async world!'


# django3以前版本实现轮训异步
# class TestAsyncioView(View):
#     def get(self, request, *args, **kwargs):
#         """
#         利用asyncio和async await关键字（python3.5之前使用yield）实现协程
#         """
#         start_time = time.time()
#         loop = asyncio.new_event_loop()  # 或 loop = asyncio.SelectorEventLoop()
#         asyncio.set_event_loop(loop)
#         self.loop = loop
#         try:
#             results = loop.run_until_complete(self.gather_tasks())
#         finally:
#             loop.close()
#         end_time = time.time()
#         return JsonResponse({'results': results, 'cost_time': (end_time - start_time)})
#
#     async def gather_tasks(self):
#         """
#          也可以用回调函数处理results
#         task1 = self.loop.run_in_executor(None, self.io_task1, 2)
#         future1 = asyncio.ensure_future(task1)
#         future1.add_done_callback(callback)
#
#         def callback(self, future):
#             print("callback:",future.result())
#         """
#         tasks = (
#             self.make_future(self.io_task1, random.random()),
#             self.make_future(self.io_task2, random.random())
#         )
#         results = await asyncio.gather(*tasks)
#         return results
#
#     async def make_future(self, func, *args):
#         future = self.loop.run_in_executor(None, func, *args)
#         response = await future
#         return response
#
#     """
#     # python3.5之前无async await写法
#     import types
#     @types.coroutine
#     # @asyncio.coroutine  # 这个也行
#     def make_future(self, func, *args):
#         future = self.loop.run_in_executor(None, func, *args)
#         response = yield from future
#         return response
#     """
#
#     def io_task1(self, sleep_time):
#         time.sleep(sleep_time)
#         return 66
#
#     def io_task2(self, sleep_time):
#         time.sleep(sleep_time)
#         return 77

