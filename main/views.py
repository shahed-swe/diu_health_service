from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponse, request
import requests
import datetime
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif request.user.is_student:
        return redirect('/patient/home')
    elif request.user.is_driver:
        return redirect('/driver/driver_home')
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
                is_moderator = True,
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
        return render(request, 'delete_moderator_view.html', {"title":"Moderator Update","assis":mod})
    else:
        return redirect('/')
# moderator crud system
def crudDriver(request):
    if request.user.is_authenticated and request.user.is_superuser:
        driver = Driver.objects.all()
        context = {'title':"Manage Driver", 'driver':driver}
        if request.method == "POST":
            user = User(
                username = request.POST.get('driverUsername'),
                first_name = request.POST.get('driverFirstname'),
                last_name = request.POST.get('driverLastname'),
                email = request.POST.get('driverEmail'),
                is_driver = True,
                is_active = True
            )
            user.set_password(request.POST.get('driverPassword1'))
            user.save()
            print(user.email)
            print(user)
            driver = Driver(
                user = user,
                driver_id = request.POST.get('driverId'),
                full_name = user.first_name+ ' '+user.last_name,
                address = request.POST.get('driverAddress'),
                age = request.POST.get('driverAge'),
                phone_no = request.POST.get('driverPhoneno')
            )
            driver.save()
            print(driver.age)
        return render(request, 'crud_driver.html',context)
    else:
        return redirect('/')

# edit view of assistant, only accessible for admin
def edit_driver(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        driver = Driver.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            driver = Driver(
                user = user,
                driver_id = request.POST.get('driverId'),
                full_name = user.first_name+ ' '+user.last_name,
                address = request.POST.get('driverAddress'),
                age = request.POST.get('driverAge'),
                phone_no = request.POST.get('driverPhoneno')
            )
            driver.save()
            return redirect('/cruddriver')
        return render(request,'edit_driver_view.html',{"title":"Update driver","driver":driver})
    else:
        return redirect('/')

# delete view of assistant, only accessible for admin
def delete_driver(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        driver = Driver.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                # print("Assistant Deleted")
                user.delete()
                driver.delete()
                # print(user, "Profile Deleted")
                return redirect('/cruddriver')
        return render(request, 'delete_driver_view.html', {"title":"Driver Update","assis":driver})
    else:
        return redirect('/')

# control information about doctor, patient and assistant of which one is assigned for whom
def control_info(request):
    if request.user.is_authenticated and request.user.is_superuser:
        doc = Doctor.objects.all()
        pat = Student.objects.all()
        assis = Assistant.objects.all()
        newdoc = AssignedDoctor.objects.all()
        newass = AssignAssistant.objects.all()
        context = {"title":"Control Info","doc":doc,"pat":pat,"assis":assis,"newdoc":newdoc,"newass":newass}
        if request.method == "POST":
            if request.POST.get('assigndoctor') == "1":
                doctor = request.POST.get('doctor1')
                patient = request.POST.get('patient1')
                if doctor != "" and patient != "":
                    assigndoc = AssignedDoctor(
                        patient = Student.objects.get(pk=patient),
                        doctor = Doctor.objects.get(pk=doctor)
                    )
                    assigndoc.save()
                    return redirect('/control_info')
            elif request.POST.get('assignassistant') == "2":
                doctor = request.POST.get('doctor2')
                assistant = request.POST.get('assistant1')
                if doctor != "" and assistant != "":
                    assignassis = AssignAssistant(
                        doctor = Doctor.objects.get(pk=doctor),
                        assistant = Assistant.objects.get(pk=assistant)
                    )
                    assignassis.save()
                    return redirect('/control_info')
        return render(request, 'control_info.html',context)
    else:
        return redirect('/')

# delete view of assigned doctor, only available for admin
def delete_assigned_doctor(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        assign_doctor = AssignedDoctor.objects.filter(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                assign_doctor.delete()
                return redirect('/control_info')
        return render(request, 'delete_assigned_doctor.html')
    else:
        return redirect('/')

# delete view of assigned assistant, only available for admin
def delete_assigned_assistant(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        assign_assistant = AssignAssistant.objects.filter(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                assign_assistant.delete()
                return redirect('/control_info')
        return render(request, 'delete_assigned_assistant.html')
    else:
        return redirect('/')

def emergency_msg(request):
    if request.user.is_authenticated and request.user.is_superuser:
        msg = EmergencyMsg.objects.all()
        context = {"msg":msg,"title":"Emergency Message"}
        return render(request, 'emergencymsg.html', context)
    else:
        return redirect('/')

def update_msg_status(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        msg = EmergencyMsg.objects.filter(pk=id).update(solve=True)
        return redirect('/emergency_msg')
    else:
        return redirect('/')

def delete_msg_status(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        msg = EmergencyMsg.objects.filter(pk = id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                msg.delete()
                # print("message deleted")
                return redirect('/emergency_msg')
        return render(request, 'delete_msg.html', {"msg":msg})
    else:
        return redirect('/')


def give_prescription(request):
    if request.user.is_authenticated and request.user.is_doctor:
        pat = Student.objects.all()
        med = Medicine.objects.all()
        assign = AssignMedicine.objects.all()
        context = {"title":"Give Prescription","patient":pat,"medicine":med,'assignedMedicine':assign}
        if request.method == 'POST':
            medic = request.POST.getlist('medicine')
            medic = [int(i) for i in medic if i != None]
            h,m,s = map(int, request.POST.get('time').split(":"))
            assin = AssignMedicine(
                student = Student.objects.get(pk = request.POST.get('patient')),
                medicine_time = datetime.time(h,m,s)
            )
            assin.save()
            for i in medic:
                assin.medicine.add(i)
            return redirect('/give_prescription')
        return render(request, 'give_prescription.html', context)

    else:
        return redirect('/')

# delete prescription view only for doctor
def delete_prescribed_data(request,id):
    if request.user.is_authenticated and request.user.is_doctor:
        assin = AssignMedicine.objects.filter(pk=id)
        if request.method == 'POST':
            val = request.POST.get('button-value')
            assin.delete()
            return redirect('/give_prescription')
        return render(request, 'delete_prescription.html',{"title":"Delete Prescription"})
    else:
        return redirect('/')

def health_condition(request):
    if request.user.is_authenticated and request.user.is_doctor:
        cns = ConditionInfo.objects.all()
        context = {"condition":cns, "title":"Patient Condition Information"}
        return render(request, 'condition_info.html', context)
    else:
        return redirect('/')

def update_condition_info(request, id):
    if request.user.is_authenticated and request.user.is_doctor:
        condition = ConditionInfo.objects.filter(id=id).update(emergency_condition=True)
        return redirect('/health_condition')
    else:
        return redirect('/')

def update_solve_info(request, id):
    if request.user.is_authenticated and request.user.is_doctor:
        condition = ConditionInfo.objects.filter(id=id).update(solve=True)
        return redirect('/health_condition')
    else:
        return redirect('/')

def update_release_info(request, id):
    if request.user.is_authenticated and request.user.is_doctor:
        condition = ConditionInfo.objects.filter(id=id)
        Student.objects.filter(pk=condition[0].patient.pk).update(released=True)
        return redirect('/health_condition')
    else:
        return redirect('/')


def delete_condition_report(request, id):
    if request.user.is_authenticated and request.user.is_doctor:
        condition = ConditionInfo.objects.filter(id=id)
        if request.method == 'POST':
            val = request.POST.get('button-value')
            condition.delete()
            # print("condition deleted")
            return redirect('/health_condition')
        return render(request, 'delete_patient_health.html',{"title":"Delete Patient Condition Information"})
    else:
        return redirect('/')

def feedback(request):
    if request.user.is_authenticated and request.user.is_doctor:
        feeds = Feedback.objects.all()
        context = {"feed":feeds,"title":"Feedbacks"}
        return render(request, 'feedbacks.html',context)
    else:
        return redirect('/')

def delete_feedbacks(request,id):
    if request.user.is_authenticated and request.user.is_doctor:
        feed = Feedback.objects.filter(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            if val == "Yes":
                feed.delete()
                return redirect('/feedbacks')
        return render(request, 'delete_feedback.html', {"feed":feed})
    else:
        return redirect('/')

def emergency_request(request):
    if request.user.is_authenticated and request.user.is_assistant:
        # this view will only show person name which condition is emergency and need to drive him to the hospital
        emergency = ConditionInfo.objects.filter(emergency_condition=True)
        return render(request, 'emergency_condition.html',{"condition":emergency})
    else:
        return redirect('/')


def set_hospital_route(request):
    if request.user.is_authenticated and request.user.is_assistant:
        driver = Driver.objects.filter(on_duty=False)
        hospital = HospitalName.objects.all()
        patient = Student.objects.all()
        route = HospitalRoute.objects.all()
        context = {"title":"Set Route For Driver", "driver":driver,"patient":patient,"hospital":hospital,"route":route}
        if request.method == "POST":
            driver = request.POST.get('driver')
            patient = request.POST.get('patient')
            hospital = request.POST.get('hospital')
            if driver != "" and hospital != "":
                new_route = HospitalRoute(
                    driver = Driver.objects.get(pk=driver),
                    patient = Student.objects.get(pk=patient),
                    hospital_name = HospitalName.objects.get(pk=hospital)
                )
                new_route.save()
                Driver.objects.filter(pk=driver).update(on_duty=True)
                Student.objects.filter(pk=patient).update(on_road=True)
                return redirect('/hospital_route')
        return render(request,'set_driver_route.html',context)
    else:
        return redirect('/')


def add_hospital_info(request):
    if request.user.is_authenticated and request.user.is_assistant:
        hospital = HospitalName.objects.all()
        context = {"title":"Hospital Information","hospital":hospital}

        if request.method == "POST":
            hospital_name = request.POST.get('hospital_name')
            hospital = HospitalName(
                hospital_name = hospital_name,
            )
            hospital.save()
        return render(request, 'hospital_info.html', context)
    else:
        return redirect('/')

def edit_hospital_name(request, id):
    if request.user.is_authenticated and request.user.is_assistant:
        hospital = HospitalName.objects.filter(pk=id)
        context = {"title":"Edit Hospital Information","hospital":hospital[0].hospital_name}
        if request.method == "POST":
            hospital_name = request.POST.get('hospital_name')
            HospitalName.objects.filter(pk=id).update(hospital_name=hospital_name)
            return redirect('/hospital_info')
        return render(request, 'edit_hospital_name.html',context)
    else:
        return redirect('/')

def delete_hospital_name(request, id):
    if request.user.is_authenticated and request.user.is_assistant:
        hospital = HospitalName.objects.filter(pk=id)
        if request.method == 'POST':
            val = request.POST.get('button-value')
            if val == "Yes":
                hospital.delete()
                return redirect('/hospital_info')
        return render(request, 'delete_hospital_name.html',{"hospital":hospital,"title":"Delete Hospital"})
    else:
        return redirect('/')


def set_billing_info(request):
    if request.user.is_authenticated and request.user.is_assistant:
        patient = Student.objects.all()
        driver = Driver.objects.filter(on_duty=True)
        bill = BillingInfo.objects.all()
        context = {"title":"Set Bill For Driver", "patient":patient,"driver":driver,"bill":bill}
        if request.method == "POST":
            pat_id = request.POST.get('patient')
            driver_id = request.POST.get('driver')
            amount = request.POST.get('amount')
            if pat_id != "" and driver_id != "" and amount != "":
                billing = BillingInfo(
                    patient = Student.objects.get(pk=pat_id),
                    driver = Driver.objects.get(pk=driver_id),
                    bill = amount
                )
                billing.save()
                return redirect('/bill_info')
        return render(request, 'set_billing_info.html', context)
    else:
        return redirect('/')

def delete_billing_info(request,id):
    if request.user.is_authenticated and request.user.is_assistant:
        bill = BillingInfo.objects.filter(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            bill.delete()
            return redirect('/bill_info')
        return render(request, 'delete_billing_info.html', {"title":"Delete Bill Information","bill":bill})
    else:
        return redirect('/')


def update_patient_bill(request,id):
    if request.user.is_authenticated and request.user.is_assistant:
        BillingInfo.objects.filter(pk=id).update(patient_paid=True)
        return redirect('/bill_info')
    else:
        return redirect('/')
    
def update_driver_bill(request,id):
    if request.user.is_authenticated and request.user.is_assistant:
        BillingInfo.objects.filter(pk=id).update(paid_driver=True)
        return redirect('/bill_info')
    else:
        return redirect('/')


def medicine_company_add(request):
    if request.user.is_authenticated and request.user.is_moderator:
        cmp = MedicineCompany.objects.all()
        if request.method == 'POST':
            mcpy = MedicineCompany(
                company_name=request.POST.get('companyName')
            )
            mcpy.save()
            return redirect('/company')
        return render(request, 'add_medicine_company.html', {"title": "Add Medicine Companies", "cmp": cmp})


# edit medicine company view, only available for moderator
def edit_medicine_company(request, id):
    if request.user.is_authenticated and request.user.is_moderator:
        cmp = MedicineCompany.objects.filter(pk=id)
        if request.method == "POST":
            cmp = MedicineCompany.objects.filter(pk=id).update(
                company_name=request.POST.get('companyName'))
            return redirect('/company')
        return render(request, 'edit_medicine_company.html', {"title": "Update", "cmp": cmp[0]})
    else:
        return redirect('/')

# delete medicine company view, only available for moderator
def delete_medicine_company(request, id):
    if request.user.is_authenticated and request.user.is_moderator:
        cmp = MedicineCompany.objects.filter(pk=id)
        if request.method == "POST":
            val = request.POST.get('button-value')
            cmp.delete()
            return redirect('/company')
        return render(request, 'delete_medicine_company.html', {"title": "Delete", "cmp": cmp[0]})
    else:
        return redirect('/')

# medicine crud view, only available for assistant


def add_medicine(request):
    if request.user.is_authenticated and request.user.is_moderator:
        med = Medicine.objects.all()
        company = MedicineCompany.objects.all()
        context = {"title": "Add Medicine", "med": med, "cmp": company}
        if request.method == "POST":
            comp = request.POST.getlist('companies')
            newcomp = [int(i) for i in comp if i != None]
            medicine = Medicine(
                medicine_name=request.POST.get('medicineName'),
            )
            medicine.save()
            for i in newcomp:
                medicine.company_name.add(i)
            return redirect('/medicine')
        return render(request, 'add_medicine.html', context)
    else:
        return redirect('/')

# delete medicine view, only available for moderator
def delete_medicine(request, id):
    if request.user.is_authenticated and request.user.is_moderator:
        med = Medicine.objects.filter(pk=id)
        if request.method == 'POST':
            val = request.POST.get('button-value')
            med.delete()
            return redirect('/medicine')
        return render(request, 'delete_medicine.html', {"title": "Delete", "med": med[0]})
    else:
        return redirect('/')

