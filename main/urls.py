from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.mylogin, name="mylogin"),
    path('logout/', views.mylogout, name="mylogout"),
    path('profile/', views.user_profile, name="user_profile"),
    path('patient/', views.patient, name="patient"),
    url(r'^edit_patient/(?P<id>.*)/$', views.edit_patient, name="edit_patient"),
    url(r'^delete_patient/(?P<id>.*)/$', views.delete_patient, name="delete_patient"),
    path('crudDoctor/', views.addDoctorInformation, name="addDoctorInformation"),
    url(r'^edit_doctor/(?P<id>.*)/$', views.edit_doctor, name="edit_doctor"),
    url(r'^delete_doctor/(?P<id>.*)/$', views.delete_doctor, name="delete_doctor"),
    path('crudAssistant/', views.crudAssistant, name="crudAssistant"),
    url(r'^edit_assistant/(?P<id>.*)/$', views.edit_assistant, name="edit_assistant"),
    url(r'^delete_assistant/(?P<id>.*)/$', views.delete_assistant, name="delete_assistant"),
    path('crudmoderator/', views.crudModerator, name="crudModerator"),
    url(r'^edit_moderator/(?P<id>.*)/$', views.edit_moderator, name="edit_moderator"),
    url(r'^delete_moderator/(?P<id>.*)/$', views.delete_moderator, name="delete_moderator"),
    path('cruddriver/', views.crudDriver, name="crudDriver"),
    url(r'^edit_driver/(?P<id>.*)/$', views.edit_driver, name="edit_driver"),
    url(r'^delete_driver/(?P<id>.*)/$', views.delete_driver, name="delete_driver"),
    path('control_info/',views.control_info, name="control_info"),
    url(r'^delete_assigned_doctor/(?P<id>.*)/$',views.delete_assigned_doctor, name="delete_assigned_doctor"),
    url(r'^delete_assigned_assistant/(?P<id>.*)/$',views.delete_assigned_assistant, name="delete_assigned_assistant"),
    path('emergency_msg/', views.emergency_msg, name="emergency_msg"),
    url(r'^update_emergency_msg/(?P<id>.*)/$',views.update_msg_status, name="update_msg_status"),
    url(r'^delete_emergency_msg/(?P<id>.*)/$',views.delete_msg_status, name="delete_msg_status"),
    path('give_prescription/', views.give_prescription,name="give_prescription"),
    url(r'^delete_prescription/(?P<id>.*)/$', views.delete_prescribed_data, name="delete_prescribed_data"),
    path('health_condition/',views.health_condition,name="health_condition"),
    url(r'^update_condition_info/(?P<id>.*)/$',views.update_condition_info,name="update_condition_info"),
    url(r'^update_solve_info/(?P<id>.*)/$',views.update_solve_info,name="update_solve_info"),
    url(r'^delete_condition_report/(?P<id>.*)/$',views.delete_condition_report, name="delete_condition_report"),
    path('feedbacks/',views.feedback, name="feedback"),
    url(r'^delete_feedback/(?P<id>.*)/$', views.delete_feedbacks, name="delete_feedbacks"),
    path('condition/',views.emergency_request,name="emergency_request"),
    path('hospital_route/', views.set_hospital_route, name="set_hospital_route"),
    path('hospital_info/',views.add_hospital_info, name="add_hospital_info"),
    url(r'^edit_hospital_name/(?P<id>.*)/$',views.edit_hospital_name, name="edit_hospital_name"),
    url(r'^delete_hospital_name/(?P<id>.*)/$',views.delete_hospital_name, name="delete_hospital_name"),
    path('bill_info/', views.set_billing_info, name="set_billing_info"),
    


]
