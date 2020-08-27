from django.urls import path
from webchat.views import chat


urlpatterns = [
    path("chat/", chat, name="chat"),
]
