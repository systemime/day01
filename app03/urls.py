from django.urls import path
from app03.views import test


urlpatterns = [
    path("test/", test, name="test"),
]
