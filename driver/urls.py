from django.urls import path
from . import views

urlpatterns = [
    path('driver_home/', views.driver, name="driver"),
    path('driver_profile/', views.driverprofile,name="driverprofile"),
    
]
