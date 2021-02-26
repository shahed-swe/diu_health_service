from django.shortcuts import render, redirect
from main.models import *
from django.http import HttpResponse

# Create your views here.
def student(request):
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
    elif request.user.is_authenticated and request.user.is_driver:
        return redirect('/')
    else:
        print(get_ip(request))
        print(request.user.first_name + ' '+request.user.last_name)
        return render(request, 'home.html', {"title":"Student | Home"})


def registration(request):
    if request.user.is_authenticated:
        return redirect('/student/home')
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password1, password2)
        if password1 == password2:
            user = User(
                username = request.POST.get('username'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
                is_student = True,
                is_active = True
            )
            user.set_password(request.POST.get('password1'))
            user.save()
            student = Student(
                user = user,
                student_id = request.POST.get('student_id'),
                full_name = user.first_name + ' ' + user.last_name,
                address = request.POST.get('address'),
                age = request.POST.get('age'),
                phone_no = request.POST.get('phone')
            )
            student.save()
        else:
            message =  "Password Doesn't match properly"
            context = {"title":"Registration","message":message}
            return render(request, 'registration.html', context)
    return render(request, 'registration.html', {'title':"Registration"})