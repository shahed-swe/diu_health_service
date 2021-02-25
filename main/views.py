from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponse
# Create your views here.
def home(request):
    print(get_ip(request))
    print(request.user.first_name + ' | '+request.user.last_name)
    return HttpResponse("Hello")



def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARD_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip
