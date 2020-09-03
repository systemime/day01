from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import View
from django.http import JsonResponse
from django.db import transaction
from django.db.transaction import on_commit
from django.contrib.auth.models import User
from app01.models import UserProfile

import json
# Create your views here.


@login_required(login_url='/webchat/login')
def chat(request):
    return render(request, "chat/index.html")


@login_required(login_url='/webchat/login')
def tailf(request):
    logDict = settings.TAILF
    print(type(logDict))
    # User.objects.create_user()
    # UserProfile.objects.create_user()
    return render(request, 'chat/tailf_index.html', {"logDict": logDict})


class Register(View):

    def get(self, request):
        return render(request, "chat/registered.html")

    def post(self, request):
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        email_list = UserProfile.objects.filter(email=email)
        print(email, "\n", email_list)

        if not email_list:
            try:
                with transaction.atomic():
                    UserProfile.objects.create_user(username=name, email=email, password=password)
            except Exception as err:
                return JsonResponse({"status": 1004, "title": "注册失败", "error": str(err)}, safe=False)
            return redirect(reverse('login-url'))
        else:
            return JsonResponse({"status": 1004, "title": '该用户已存在！', "error": '请重新注册'}, safe=False)
