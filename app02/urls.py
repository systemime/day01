from django.urls import path
from app02.views import test, test_signal
from django.views.decorators.gzip import gzip_page


urlpatterns = [
    path("test/", gzip_page(test), name="test"),
    path("test_signal/", gzip_page(test_signal), name="test_signal"),
]
