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
    obj = Student.objects.all()
    cnt = 0
    for i in obj:
        if i.released == True:
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


# user profile
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'user_profile.html', {"title":"{} Profile".format(request.user.username.title())})
    else:
        return redirect('/')

# only for student information controlling
def patient(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif request.user.is_superuser:
        patient = Student.objects.all()
        return render(request, 'patient_control.html',{'title':"Student","patient":patient})
    else:
        return redirect('/')

def edit_patient(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif request.user.is_superuser:
        pat = Student.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            if request.POST.get('patientRelease') == 'on':
                patient = Student(
                    user = user,
                    full_name = user.first_name+ ' '+ user.last_name,
                    address = request.POST.get('patientAddress'),
                    age = request.POST.get('patientAge'),
                    phone_no = request.POST.get('patientPhoneno'),
                    released = True 
                )
                patient.save()
            else:
                patient = Student(
                    user=user,
                    full_name=user.first_name + ' ' + user.last_name,
                    address=request.POST.get('patientAddress'),
                    age=request.POST.get('patientAge'),
                    phone_no=request.POST.get('patientPhoneno'),
                    released=False
                )
                patient.save()
            return redirect('/patient')
        return render(request, 'edit_patient_view.html',{'title':"Edit {}".format(user.username),"pat":pat})
    else:
        return redirect('/')

def delete_patient(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif request.user.is_superuser:
        patient = Student.objects.filter(pk=id)
        user = User.objects.filter(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                print("Patient Deleted")
                patient.delete()
                user.delete()
                return redirect('/patient')
        return render(request, 'delete_patient_view.html',{"title":"Delete","patient":patient})
    else:
        return redirect('/')

# crud system for admin who will control all of doctor's credentials
def addDoctorInformation(request):
    if request.user.is_authenticated and request.user.is_superuser:
        doctor = Doctor.objects.all()
        context = {"title":"Doctor Information","doc":doctor}

        if request.method == "POST":
            user = User(
                username = request.POST.get('doctorUsername'),
                first_name = request.POST.get('doctorFirstname'),
                last_name = request.POST.get('doctorLastname'),
                email = request.POST.get('doctorEmail'),
                is_doctor = True,
                is_active = True
            )
            user.set_password(request.POST.get('doctorPassword1'))
            user.save()
            doctor = Doctor(
                user = user,
                employee_id = request.POST.get('doctorId'),
                full_name = user.first_name + ' ' + user.last_name,
                address = request.POST.get('doctorAddress'),
                age = request.POST.get('doctorAge'),
                phone_no = request.POST.get('doctorPhoneno')
            )
            doctor.save()
        return render(request, 'crud_doctor.html', context)
    else:
        return redirect('/')


def edit_doctor(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        doc = Doctor.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            doctor = Doctor(
                user = user,
                employee_id = request.POST.get('doctorId'),
                full_name = user.first_name + ' ' +user.last_name,
                address = request.POST.get('doctorAddress'),
                age = request.POST.get('doctorAge'),
                phone_no = request.POST.get('doctorPhoneno'),
            )
            doctor.save()
            return redirect('/crudDoctor')
        return render(request, 'edit_doctor_view.html',{"title":"Edit Doctor","doc":doc})
    else:
        return redirect('/')

def delete_doctor(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        doc = Doctor.objects.filter(pk=id)
        user = User.objects.filter(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                print("Doctor Credentials deleted")
                doc.delete()
                user.delete()
                return redirect('/crudDoctor')
        return render(request, 'delete_doctor_view.html', {"title":"Delete Credentials","doc":doc})
    else:
        return redirect('/')

def crudAssistant(request):
    if request.user.is_authenticated and request.user.is_superuser:
        assis = Assistant.objects.all()
        context = {'title':"Manage Assistant", 'assistant':assis}
        if request.method == "POST":
            user = User(
                username = request.POST.get('assistantUsername'),
                first_name = request.POST.get('assistantFirstname'),
                last_name = request.POST.get('assistantLastname'),
                email = request.POST.get('assistantEmail'),
                is_assistant = True,
                is_active = True
            )
            user.set_password(request.POST.get('assistantPassword1'))
            user.save()
            # print(user.password)
            # print(user)
            assistant = Assistant(
                user = user,
                assistant_id = request.POST.get('assistantId'),
                full_name = user.first_name+ ' '+user.last_name,
                address = request.POST.get('assistantAddress'),
                age = request.POST.get('assistantAge'),
                phone_no = request.POST.get('assistantPhoneno')
            )
            # print(assistant)
            assistant.save()
        return render(request, 'crud_assistant.html',context)
    else:
        return redirect('/')

# edit view of assistant, only accessible for admin
def edit_assistant(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        assis = Assistant.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            assistant = Assistant(
                user = user,
                assistant_id = request.POST.get('assistantId'),
                full_name = user.first_name+ ' '+user.last_name,
                address = request.POST.get('assistantAddress'),
                age = request.POST.get('assistantAge'),
                phone_no = request.POST.get('assistantPhoneno')
            )
            assistant.save()
            # print(assistant.assistant_id)
            return redirect('/crudAssistant')
        return render(request,'edit_assistant_view.html',{"title":"Update Assistant","assis":assis})
    else:
        return redirect('/')

# delete view of assistant, only accessible for admin
def delete_assistant(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        assis = Assistant.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                # print("Assistant Deleted")
                user.delete()
                assis.delete()
                return redirect('/crudAssistant')
        return render(request, 'delete_assistant_view.html', {"title":"Assistant Update","assis":assis})
    else:
        return redirect('/')

# moderator crud system
def crudModerator(request):
    if request.user.is_authenticated and request.user.is_superuser:
        mod = Moderator.objects.all()
        context = {'title':"Manage Moderator", 'moderator':mod}
        if request.method == "POST":
            user = User(
                username = request.POST.get('moderatorUsername'),
                first_name = request.POST.get('moderatorFirstname'),
                last_name = request.POST.get('moderatorLastname'),
                email = request.POST.get('moderatorEmail'),
                is_assistant = True,
                is_active = True
            )
            user.set_password(request.POST.get('moderatorPassword1'))
            user.save()
            moderator = Moderator(
                user = user,
                moderator_id = request.POST.get('moderatorId'),
                full_name = user.first_name+ ' '+user.last_name,
                address = request.POST.get('moderatorAddress'),
                age = request.POST.get('moderatorAge'),
                phone_no = request.POST.get('moderatorPhoneno')
            )
            moderator.save()
        return render(request, 'crud_moderator.html',context)
    else:
        return redirect('/')

# edit view of assistant, only accessible for admin
def edit_moderator(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        mod = Moderator.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            moderator = Moderator(
                user = user,
                moderator_id = request.POST.get('moderatorId'),
                full_name = user.first_name+ ' '+user.last_name,
                address = request.POST.get('moderatorAddress'),
                age = request.POST.get('moderatorAge'),
                phone_no = request.POST.get('moderatorPhoneno')
            )
            moderator.save()
            return redirect('/crudmoderator')
        return render(request,'edit_moderator_view.html',{"title":"Update Moderator","mod":mod})
    else:
        return redirect('/')

# delete view of assistant, only accessible for admin
def delete_moderator(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        mod = Moderator.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                # print("Assistant Deleted")
                user.delete()
                mod.delete()
                return redirect('/crudmoderator')
        return render(request, 'delete_assistant_view.html', {"title":"Assistant Update","assis":mod})
    else:
        return redirect('/')