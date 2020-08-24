from django.shortcuts import render

# Create your views here.

from django.views.generic.base import TemplateView
from app04.connection import WebSocket


class IndexView(TemplateView):
    template_name = "tell.html"


async def websocket_view(socket: WebSocket):
    # import pdb;pdb.set_trace()
    await socket.accept()
    while True:
        message = await socket.receive_text()
        print(message)
        await socket.send_text(message if message else "")
