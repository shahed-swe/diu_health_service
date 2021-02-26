from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponse
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif request.user.is_student:
        return redirect('/patient/home')
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

# this is for login panel
def mylogin(request):
    print(get_ip(request))
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        utxt = request.POST.get('username')
        upass = request.POST.get('password')
        if utxt != '' and upass != '':
            user = authenticate(username=utxt, password=upass)
            if user != None:
                login(request, user)
                return redirect('/')
        else:
            return redirect('/login')
    context = {"title": "Login"}
    return render(request, 'login.html', context)

# this is for logout panel
def mylogout(request):
    logout(request)
    return redirect('/login')