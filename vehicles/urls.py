from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls import url
from . import views
print("ciao")
urlpatterns = [
	path('',views.index, name='index'),
	path('register',views.register, name='register'),
	path('logout',views.logout, name='logout'),
	path('accounts/login/register',views.register, name='register'),
	path('<vehicleID>',views.vehiclesDetails, name='vehiclesDetails'),
	url('deletebooking?bookingid=<int:bookid>',views.bookingDelete, name='bookingDelete')
]