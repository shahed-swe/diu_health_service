from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    

    def __str__(self):
        return self.first_name + ' | '+str(self.pk)

class Doctor(models.Model):
    employee_id = models.CharField(max_length=120, blank=True, null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="doctor")
    full_name = models.CharField(max_length=200,blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    age = models.CharField(max_length=3, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        db_table = "doctor_info"

    def __str__(self):
        return self.full_name

class Student(models.Model):
    student_id = models.CharField(max_length=120,blank=True, null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="student")
    full_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'student_info'
    
    def __str__(self):
        return self.full_name

class Moderator(models.Model):
    moderator_id = models.CharField(max_length=120, blank=True, null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="moderator")
    full_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'moderator_info'

    def __str__(self):
        return self.full_name

class Assistant(models.Model):
    assistant_id = models.CharField(max_length=120, blank=True, null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="assistant")
    full_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'assistant_info'

    def __str__(self):
        return self.full_name

class Driver(models.Model):
    driver_id = models.CharField(max_length=120, blank=True, null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="driver")
    full_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "driver_info"

    def __str__(self):
        return self.full_name

class MedicineCompany(models.Model):
    company_name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'medicine_company'

    def __str__(self):
        return self.company_name


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=120, blank=True, null=True)
    company_name = models.ManyToManyField(MedicineCompany, related_name='company')

    class Meta:
        db_table = 'medicine_info'

    def __str__(self):
        return self.medicine_name

# this class has been made only for patient
class ConditionInfo(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Student, on_delete=models.CASCADE)
    patient_condition = models.CharField(max_length=300, blank=True, null=True)
    emergency_condition = models.BooleanField(default=False)
    solve = models.BooleanField(default=False)

    class Meta:
        db_table = 'condition_info'

    def __str__(self):
        return self.patient.full_name

# this class has been made only for patient
class AssignedDoctor(models.Model):
    patient = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True, related_name="doctor")

    class Meta:
        db_table = "assigned_doctor"

    def __str__(self):
        return self.patient.full_name + '-->' + self.doctor.full_name

class BillingInfo(models.Model):
    patient = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    bill = models.CharField(max_length=120,blank=True, null=True)
    patient_paid = models.BooleanField(default=False)
    paid_driver = models.BooleanField(default=False)

    class Meta:
        db_table = "billing_info"

    def __str__(self):
        return self.patient.full_name + " | "+self.bill

class HospitalName(models.Model):
    hospital_name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = "hospitals"

    def __str__(self):
        return self.hospital_name

class AssignAssistant(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, primary_key=True)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, blank=True, null=True, related_name="assistant")

    class Meta:
        db_table = "assigned_assistant"

    def __str__(self):
        return self.doctor.full_name + " " + self.assistant.full_name

    
class HospitalRoute(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, primary_key=True)
    hospital_name = models.ForeignKey(HospitalName, on_delete=models.CASCADE, blank=True, null=True)
    driver_spotted = models.BooleanField(default=False)

    class Meta:
        db_table = 'hospital_route'

    def __str__(self):
        return self.driver.full_name