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
]
