from django.utils.deprecation import MiddlewareMixin  # 3.1开始MiddlewareMixin支持异步请求，可用于拓展
from django.utils.decorators import sync_and_async_middleware
from django.utils.decorators import method_decorator

import asyncio


class App03Middle(MiddlewareMixin):

    def process_request(self, request):
        print("请求开始")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("开始处理视图")

    def process_response(self, request, response):
        print("响应结束")
        return response

    def process_exception(self, request, process_exception):
        print("开始进行错误处理")


# # django3.1中示例的支持同步/异步请求的混合中间件
# # 暂时不知道如何添加到django的自定义中间件中
# @sync_and_async_middleware
# def simple_middleware(get_response):
#     # One-time configuration and initialization goes here.
#     if asyncio.iscoroutinefunction(get_response):
#         async def middleware(request):
#             # Do something here!
#             print("111111111111111111111")
#             # Do something here!
#             response = await get_response(request)
#             return response
#
#     else:
#         def middleware(request):
#             # Do something here!
#             print("222222222222222222222")
#             # Do something here!
#             response = get_response(request)
#             return response
#
#     return middleware
