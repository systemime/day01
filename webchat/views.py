from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import json
# Create your views here.


@login_required(login_url='/webchat/login')
def chat(request):
    return render(request, "chat/index.html")


@login_required(login_url='/webchat/login')
def tailf(request):
    logDict = settings.TAILF
    print(type(logDict))
    return render(request, 'chat/tailf_index.html', {"logDict": logDict})
