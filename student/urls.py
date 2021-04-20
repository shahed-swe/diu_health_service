from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.patient, name="patient"),
    path('myregistration/', views.registration, name="registration"),
    path('profile/', views.profile, name="profile"),
    path('medicine/', views.medicine, name="medicine"),
    path('pat_feedback/', views.patfeedback, name="patfeedback"),
    path('message/', views.emg_msg, name="emg_msg"),
    path('driver/', views.patdriver, name="patdriver"),
]
