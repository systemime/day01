from django.urls import path
from webchat.views import chat, tailf, Register
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("chat/", chat, name="chat"),
    path('tailf/', tailf, name='tailf-url'),
    path('login/', LoginView.as_view(template_name='chat/login.html'), name='login-url'),
    path('logout/', LogoutView.as_view(template_name='chat/login.html'), name='logout-url'),
    path('register/', Register.as_view(), name='register-url'),
]
