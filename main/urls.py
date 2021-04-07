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
]
