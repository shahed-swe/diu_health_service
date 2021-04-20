from main.views import feedback
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from main.models import *
from django.http import HttpResponse
# Create your views here.


def patient(request):
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
        return redirect('/driver/home')
    else:
        print(get_ip(request))
        print(request.user.first_name + ' ' + request.user.last_name)
        return render(request, 'home.html', {"title": "Patient | Home"})


def registration(request):
    if request.user.is_authenticated:
        return redirect('/patient/home')
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password1, password2)
        if password1 == password2:
            user = User(
                username=request.POST.get('username'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                is_patient=True,
                is_active=True
            )
            user.set_password(request.POST.get('password1'))
            user.save()
            patient = Student(
                user=user,
                full_name=user.first_name + ' ' + user.last_name,
                address=request.POST.get('address'),
                age=request.POST.get('age'),
                phone_no=request.POST.get('phone')
            )
            patient.save()
            Token.objects.create(user=user)
        else:
            message = "Password Doesn't match properly"
            context = {"title": "Registration", "message": message}
            return render(request, 'registration.html', {'title': 'Registration'})
    return render(request, 'registration.html', {"title": 'Registration'})


def profile(request):
    if request.user.is_authenticated and request.user.is_student:
        pat = Student.objects.filter(pk=request.user.pk)
        medicines = AssignMedicine.objects.filter(student=pat[0].user.pk)
        report = ConditionInfo.objects.filter(patient=pat[0].user.pk)
        bill = BillingInfo.objects.filter(patient=pat[0].user.pk)
        hospitalroute = HospitalRoute.objects.filter(patient=pat[0].user.pk, deliverd=False)
        doctors = AssignedDoctor.objects.filter(patient=pat[0].user.pk)
        medicines_new = []
        for i in medicines:
            for j in i.medicine.all():
                if j.medicine_name not in medicines_new:
                    medicines_new.append(j.medicine_name)
        context = {"title": "Profile | {}".format(pat[0].full_name), 'patient': pat[0], 'medicine_name': medicines_new, 'report': report, 'bill': bill, 'doctor': doctors,'hosp':hospitalroute}
        return render(request, 'patient_profile.html', context)
    else:
        return redirect('/patient/home')


def medicine(request):
    if request.user.is_authenticated and request.user.is_student:
        medicines = AssignMedicine.objects.filter(student=request.user.pk)
        print(medicines)
        context = {"title": "Medicines", 'medicine': medicines}
        return render(request, 'medicines.html', context)


def patfeedback(request):
    if request.user.is_authenticated and request.user.is_student:
        if request.method == 'POST':
            feed = Feedback(
                student=Student.objects.get(pk=request.user.pk),
                feedback=request.POST.get('feedback'),
            )
            feed.save()
            
            return redirect('/patient/pat_feedback')
        feedbacks = Feedback.objects.filter(student=request.user.student)
        return render(request, 'feedback.html', {"title": "Feedback","feeds":feedbacks})
    else:
        return redirect('/patient/home')


def emg_msg(request):
    if request.user.is_authenticated and request.user.is_student:
        if request.method == 'POST':
            emg = EmergencyMsg(
                student=Student.objects.get(pk=request.user.pk),
                message=request.POST.get('message'),
                solve = False
            )
            emg.save()
            
            return redirect('/patient/message')
        emg_message = EmergencyMsg.objects.filter(student=request.user.student,solve=False)
        return render(request, 'emergency_message.html', {"title": "Emergency","emgs":emg_message})
    else:
        return redirect('/patient/home')

def driver(request):
    if request.user.is_authenticated and request.user.is_student:
        student = request.user.student
        stu_route = HospitalRoute.objects.filter(patient=student)
        if stu_route[0].deliverd == True:
            return redirect('/patient/home')
        if request.method == "POST":
            route = HospitalRoute.objects.filter(patient=student)
            print(route[0].driver.pk)
            Driver.objects.filter(pk=route[0].driver.pk).update(on_duty=False)
            route.update(deliverd=True)
            return redirect('/patient/home')
        return render(request, 'driver_spotted.html', {"title":"Driver Position"})
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
