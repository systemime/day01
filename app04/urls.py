from django.urls import path
from app04 import views


urlpatterns = [
    path("", views.IndexView.as_view()),
    path("ws/", views.websocket_view),  # 自建Websocket类实现方式
]
