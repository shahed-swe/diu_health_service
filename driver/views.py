from main.views import feedback
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from main.models import *
from django.http import HttpResponse
# Create your views here.


def driver(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif request.user.is_authenticated and request.user.is_superuser:
        return redirect('/')
    elif request.user.is_authenticated and request.user.is_doctor:
        return redirect('/')
    elif request.user.is_authenticated and request.user.is_moderator:
        return redirect('/')
    elif request.user.is_authenticated and request.user.is_assistant:
        return redirect('/')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('/patient/home')
    else:
        print(get_ip(request))
        print(request.user.first_name + ' ' + request.user.last_name)
        return render(request, 'home.html', {"title": "Driver | Home"})



def driverprofile(request):
    if request.user.is_authenticated and request.user.is_student:
        context = {"title": "Profile | {}".format(request.user.driver.full_name)}
        return render(request, 'driver_profile.html', context)
    else:
        return redirect('/patient/home')



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
