from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['username', 'is_doctor','is_student','is_moderator','is_assistant','is_driver','is_active','is_superuser']

admin.site.unregister(Group)
admin.site.register(Doctor)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Moderator)
admin.site.register(Assistant)
admin.site.register(Driver)
# 
admin.site.register(MedicineCompany)
admin.site.register(Medicine)
admin.site.register(ConditionInfo)
admin.site.register(AssignedDoctor)
admin.site.register(BillingInfo)
admin.site.register(HospitalName)
admin.site.register(AssignAssistant)
admin.site.register(HospitalRoute)
admin.site.register(AssignMedicine)
admin.site.register(EmergencyMsg)
