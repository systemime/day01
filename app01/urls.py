from django.urls import path
# Gzip
from django.views.decorators.gzip import gzip_page
from app01.views import Index, TornAsyncioView, Testasync, Testsync
from app01.views import current_datetime, async_celery


urlpatterns = [
    path("index/", gzip_page(Index.as_view()), name="index"),
    path("example/", current_datetime, name="example"),
    path("async/", Testasync.as_view(), name="async"),
    path("sync/", Testsync.as_view(), name="sync"),
    path("torn/", TornAsyncioView.as_view(), name="torn"),
    path("async_celery/", async_celery, name="async_celery"),
]
