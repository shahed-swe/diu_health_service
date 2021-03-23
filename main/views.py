from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponse
import requests
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    # elif request.user.is_student:
    #     return redirect('/')
    print(get_ip(request))
    print(request.user.first_name+' '+request.user.last_name)
    total_user = len(User.objects.all())
    total_patient = len(Student.objects.all())
    total_medicine = len(Medicine.objects.all())
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    api_key = "ec47c902d7798b639246714c56a0d4ef"
    city = 'Tangail'
    city_weather = requests.get(url.format(city, api_key)).json()
    # print(city_weather)
    weather = {
        'city': city,
        'temperature': int(city_weather['main']['temp']) // 10,
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
    }
    bill = total_bill(BillingInfo.objects.all())
    print(bill)
    problem = len(EmergencyMsg.objects.all())
    released = total_released_student()
    doctors = len(Doctor.objects.all())
    assistant = len(Assistant.objects.all())
    assignedassistant = len(AssignAssistant.objects.all())
    assigneddoctor = len(AssignedDoctor.objects.all())
    slv = len(EmergencyMsg.objects.filter(solve=False))
    context = {
        'total_user' : total_user,
        "total_patient" : total_patient,
        "total_medicine": total_medicine,
        "weather": weather,
        "title":"DIU Heath Service",
        'total_bill' : bill,
        "total_problem":problem,
        "total_released":released,
        "total_doctors":doctors,
        "total_assistant": assistant,
        "assign_nurse":assignedassistant,
        "assign_doc":assigneddoctor,
        "solve":slv,
    }
    return render(request, 'home_page.html', context)

def total_released_student():
    obj = ConditionInfo.objects.all()
    cnt = 0
    for i in obj:
        if i.solve == True:
            cnt += 1
    
    return cnt


def total_bill(take):
    bill_summation = 0
    for i in take:
        bill_summation += int(i.bill)
    return bill_summation

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
