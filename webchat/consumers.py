from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from webchat.tasks import tailf, tailf_tail


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = args[0]['url_route']['kwargs']['room']

    async def connect(self):
        if self.scope['user'].is_anonymous:
            # 拒绝匿名用户连接
            await self.close()
        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(  # 放到一个组里
            self.room_group_name,
            {
                'type': 'chat_message',  # 指定了消息处理函数
                'message': message
            }
        )

    # Receive message from room group
    # 操作都是在self.room_group_name组内进行
    async def chat_message(self, event):
        print(event)
        # user = self.scope['user'].get_username()
        user = self.scope['user'].name
        message = user + ":  " + event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class TailfConsumer(WebsocketConsumer):
    def connect(self):
        self.file_id = self.scope["url_route"]["kwargs"]["id"]

        # 这里其实并不适合使用celery监控，实时查看监控可能处在一个较长的时间
        # celery task任务在--time-limit设置的超时时间后，硬性结束标记任务超时
        # 目前修改超时为2小时
        self.result = tailf_tail.delay(self.file_id, self.channel_name)

        print('connect:', self.channel_name, self.result.id)
        self.accept()

    def disconnect(self, close_code):
        # 中止执行中的Task
        self.result.revoke(terminate=True)
        print('disconnect:', self.file_id, self.channel_name)

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))
