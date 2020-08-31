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
# 数据库事务
from django.db import transaction
from django.db.transaction import on_commit
# 跳转
from django.http import HttpResponseRedirect
#
from django.template.context import RequestContext
# 模型查询并返回http
from django.shortcuts import get_object_or_404

# 日志控制
import logging

# 异步包装
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from aiohttp import ClientSession

# 模型
from app01.models import UserProfile, UserLog
# 任务
from app01.hand import Hand
from day01.celery import async_task
from app01.tasks import select, event_log, my_task1, my_task2, my_task3, add
# celery组，签名
from celery import group, signature
# 日志处理
from celery.utils.log import get_logger
logger = get_logger(__name__)

import requests
import random
import asyncio
import aiohttp
import datetime
import types
import json


async def async_celery(request):
    """
    :type test
    :content celery 签名、组任务等，异步视图中获取同步线程中异步任务结果
    """
    # t1 = signature(my_task1, args=(1, 2))
    # t2 = signature(my_task2, args=(1, 2))
    # t3 = signature(my_task3, args=(1, 2))
    # t4 = signature(select, args=(1, ))
    # my_group = group(t1, t2, t3, t4).apply_async(queue='select_queue')
    # res = my_group.get()

    try:
        t4 = select.apply_async((1,))
        res = await sync_to_async(t4.get)()  # 空括号实例化SynctoAsync对象，获取返回内容
    except Exception as err:
        res = {
            "code": 502,
            "status": "异步任务出现错误",
            "error": str(err)
        }
    if not isinstance(res.get('res'), str):
        res = {
            "code": 502,
            "status": "异步任务错误，其类型为 %s" % type(res.get('res'))
        }

    # # 获取该任务的实例化对象，参数task_id
    # ret = select.apply_async((1, ), queue='select_queue', countdown=1)
    # res = async_task.AsyncResult(ret)
    # print(res.status)

    # # 分块 https://docs.celeryproject.org/en/stable/userguide/canvas.html#chunks
    # # 分块可让您将可重复的工作分成多个部分，这样，如果您有一百万个对象，则可以创建10个任务，每个任务有十万个对象。
    # # 有些人可能会担心将任务分块会导致并行度降低，但是对于繁忙的集群而言，情况很少如此，
    # # 实际上，因为避免了消息传递的开销，这可能会大大提高性能。
    # res = add.chunks(zip(range(100), range(100)), 10)()
    # print(res.get())
    # # apply_async将创建一个专用任务，以便将各个任务应用在工作程序中
    # add.chunks(zip(range(100), range(100)), 10).apply_async()
    # # 您还可以将块转换为组：
    # group = add.chunks(zip(range(100), range(100)), 10).group()
    # # 并且随着组的倾斜，每个任务的倒数以1为增量：
    # # 这意味着第一个任务的倒计时为一秒，第二个任务的倒计时为两秒，依此类推。
    # group.skew(start=1, stop=10)()

    # # 对任务对撤销
    # result.revoke()
    # AsyncResult(id).revoke()
    # app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed', terminate=True, signal='SIGKILL')

    # # 回调
    # # 首先执行(2, 2)计算，计算结果与16再次使用add计算
    # # add.s是签名, retry为false不重试
    # add.apply_async((2, 2), link=add.s(16), retry=True, retry_policy={
    #     'max_retries': 3,  # 放弃之前的最大重试次数，将引发导致重试失败的异常。 值None意味着它将永远重试。 默认为重试3次。
    #     'interval_start': 0,  # 定义两次重试之间要等待的秒数（浮点数或整数）。默认值为0（第一次重试将立即执行）
    #     'interval_step': 0.2,  # 每次连续重试时，此数字将被添加到重试延迟中（浮点数或整数）。默认值为0.2
    #     'interval_max': 0.2,  # 重试之间等待的最大秒数（浮点数或整数）。默认值为0.2
    # })

    # # 错误处理，retry=false时，任务失败立即发生该异常
    # try:
    #     add.delay(2, 2)
    # except add.OperationalError as exc:
    #     logger.exception('Sending task raised: %r', exc)

    # # 压缩： https://docs.celeryproject.org/en/stable/userguide/calling.html?highlight=group#compression
    # add.apply_async((2, 2), compression='zlib')

    return JsonResponse(res)
    # return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json")


# @transaction.atomic  # 在异步视图中，同步的数据库事务装饰器可能存在问题
async def tran_handler(request):
    """
    view type：test
    content：数据库事务 celery异步 视图异步
    """

    def create_db():
        try:
            with transaction.atomic():
                article = UserLog.objects.create(
                    name="测试",
                    info="测试视图"
                )
            return article.pk
        except Exception as err:
            return err

    article = await sync_to_async(create_db)()
    # https://docs.celeryproject.org/en/stable/userguide/tasks.html#database-transactions
    # 如果任务在提交事务之前开始执行，则存在竞争条件。
    # on_commit成功提交所有事务后，使用回调启动您的Celery任务 django version > 1.9
    # 但是on_commit无法返回匿名函数结果，忽略装饰器，使用with语法保证异步效率
    sync_to_async(on_commit(lambda: select.delay(article if article == 1 else 1)))

    res = await sync_to_async(select.apply_async((article if article == 1 else 1,)).get)()
    # print(res.keys())
    # return HttpResponseRedirect('/app01/example/')
    return HttpResponse("OK")


# @method_decorator(gzip_page, name='dispatch')  # 装饰整个类
class Index(View):
    # 私有缓存控制 1，请求方法限制，缓存并缓存时间
    get_decorators = [cache_control(private=True), require_http_methods(['GET', ]), cache_page(60 * 15)]

    # @method_decorator(patch_cache_control())
    @method_decorator(get_decorators)
    def get(self, request):
        # django-redis 锁/支持分布式
        # ----- 有问题 -----
        # with cache.lock("my_key"):
        #     name = cache.get('my_key')
        #     # cache.get_many(['a', 'b', 'c'])
        #     # cache.delete('xxx')
        #     # cache.delete_many(['a', 'b', 'c'])
        #     # cache.clear()
        #     # # 重新设置过期时间
        #     cache.touch('my_key', 60 * 15)
        #     # # 缓存增 1
        #     # cache.incr(key, delta=1, version=None)
        #     # # 缓存减 1
        #     # cache.decr(key, delta=1, version=None)

        logger = logging.getLogger(__name__)
        logger.info('Something went send!')

        context = {
            "key": "asdfo23jhj45k2l",
            "msg": "你好",
            "name": "xxx"
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
    @staticmethod
    def get_username():
        user = UserProfile.objects.last()
        return user.username

    def current_datetime(self, request):
        now = datetime.datetime.now()
        data = requests.get("https://www.baidu.com").text

        username = Testsync.get_username()
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


def request_def(request):
    result = get_object_or_404(UserLog, pk=1).name
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip, result)
    html = []
    tuple_dict = request.META.items()
    for k, v in tuple_dict:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))

    return HttpResponse('<table>%s</table>' % '\n'.join(html))
