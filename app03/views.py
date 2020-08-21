from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from asgiref.sync import sync_to_async
from django.views.decorators.gzip import gzip_page
# Create your views here.
from app01.models import UserProfile


async def test(request):
    user = await sync_to_async(UserProfile.objects.first)()
    print(user)
    return render(request, "text.html")


