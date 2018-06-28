from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as django_logout
from vehicles.models import Booking
from vehicles.models import Vehicles


def logout(request):
	django_logout(request)
	return redirect('index')


@csrf_exempt
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = UserCreationForm()
	context = {'form':form}
	return render(request, 'registration/register.html', context)


def index(request):
	if request.user.is_authenticated:
		userid = request.user.id
		bookingList = mapBookings(userid)
		vehiclesList = mapVehicles()
		context = {'BookingList':bookingList,'VehiclesList':vehiclesList}
	else:
		context = {}    
	return render(request, 'vehicles/index.html', context)


def mapBookings(userid):
	bookings = []
	bookedvehicles = Booking.objects.filter(userid=userid)
	for booking in bookedvehicles:
		print(booking)
		model = Vehicles.objects.get(vehiclesid=booking.vehiclesid)
		bookings.append({
			'UserID':booking.userid,
			'Model':model.model,
			'StartDate':booking.startdate,
			'EndDate':booking.enddate,
			'Place':booking.place,
		})
	return bookings

def mapVehicles():
	vehicles = []
	getVehicles = Vehicles.objects.all()
	for vehicle in getVehicles:
		vehicles.append({
			'VehicleID':vehicle.vehiclesid,
			'Code':vehicle.code,
			'Model':vehicle.model,
		})
	return vehicles

@login_required
def vehiclesDetails(request, vehicleID):
	userid = request.user.id
	username = request.user.username
	msg = ""
	if request.method == 'POST':
		enddate = request.POST['enddate']
		startdate = request.POST['startdate']
		place = request.POST['place']
		msg = bookVehicle(vehicleID,userid, enddate, startdate, place)
	vehiclesData = Vehicles.objects.get(vehiclesid=vehicleID)
	vehiclesInfo = [vehiclesData.code, vehiclesData.model]
	vehicleBookedList = vehicleBooking(vehicleID,userid,username)

	return render(request, 'vehicles/vehicledetails.html', {'VehiclesInfo':vehiclesInfo,'VehicleBookedList':vehicleBookedList, 'msg':msg})

def	vehicleBooking(vehicleID,userid,username):
	vehicleBookedList = []
	bookingList = Booking.objects.filter(vehiclesid=vehicleID, userid=userid)
	for booked in bookingList:
		model = Vehicles.objects.get(vehiclesid=booked.vehiclesid)
		vehicleBookedList.append({
			'bookid':booked.bookid,
			'username':username,
			'vehiclesid':booked.vehiclesid,
			'model':model.model,
			'startdate':booked.startdate,
			'enddate':booked.enddate,
			'place':booked.place,
		})
	return vehicleBookedList

def bookVehicle(vehicleID,userid, enddate, startdate, place):
	bookingByVehicle = Booking.objects.filter(vehiclesid=vehicleID)
	notAviable = False
	for row in bookingByVehicle:
		if(str(row.startdate) <= startdate <=  str(row.enddate) or str(row.startdate) <= enddate <=  str(row.enddate)):
			notAviable = True
	if notAviable == True:
		return "The car is not aviable in this period"
	else:
		booking = Booking(
			userid=userid,
			vehiclesid=vehicleID,
			startdate=startdate,
			enddate=enddate,
			place=place
		)
		booking.save()
		return "Booked"

def bookingDelete(request):
	print("sucooooo")
	return render(request, 'vehicles/vehicledetails.html')
