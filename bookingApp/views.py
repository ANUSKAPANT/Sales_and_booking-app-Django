
from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError


from .models import *
from .forms import *
from .decorators import *

# Create your views here.

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)  
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')	
	context = {'form':form}
	return render(request, 'template/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('services')
		else:
			messages.info(request, 'Username OR password is incorrect')
	context = {}
	return render(request, 'template/login.html', context)



def logoutUser(request):
	logout(request)
	return redirect('login')



def servicesView(request):
	services = Service.objects.all();
	context={'services':services}
	return render(request,'template/services.html', context);


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])

def createServiceView(request):
	form = ServiceForm()
	if request.method == 'POST':
		form = ServiceForm(request.POST)
		if form.is_valid():
			service = form.save(commit=False)
			service.seller = Customer.objects.get(user=request.user)  
			service.save()
			return redirect('services')
	context={'form': form}
	return render(request, 'template/create_service.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])

def bookingView(request, pk):
	service = Service.objects.get(id=pk);
	form = BookingForm()
	if request.method == 'POST':
		form = BookingForm(request.POST)
		if form.is_valid:
			booking = form.save(commit=False)
			booking.service = service
			booking.buyer = Customer.objects.get(user=request.user)
			try:  
				booking.save()
				return redirect('user-profile')
			except IntegrityError as e:
				e = 'Timeslot already booked!'
				return render(request,"template/booking.html", {"message": e, "form": form})
	return render(request,"template/booking.html", {"form": form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])

def updateBooking(request, pk):
	booking = Booking.objects.get(id=pk)
	form = BookingForm(instance = booking)
	if request.method == 'POST':
		form = BookingForm(request.POST, instance=booking)
		if form.is_valid():
			form.save()
			return redirect('user-profile')
	context = {'form':form}
	return render(request, 'template/update_booking.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])

def deleteBooking(request, pk):
	booking = Booking.objects.get(id=pk)
	if request.method == "POST":
		booking.delete()
		return redirect('user-profile')
	context = {'item':booking}
	return render(request, 'template/delete_booking.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def infoView(request):
	customers = Customer.objects.all()
	services = Service.objects.all()
	bookings = Booking.objects.all()
	total_bookings = bookings.count()
	total_services = services.count()
	total_customers = customers.count()
	context = {'services':services , 'bookings' : bookings, 'total_bookings':total_bookings, 'total_services':total_services, 
			'total_customers' : total_customers}
	return render(request, 'template/info.html', context);


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])

def userProfile(request):
	img = request.user.customer.profile_pic.url
	customer = request.user.customer
	services = Service.objects.filter(seller=customer)
	bookings = Booking.objects.filter(buyer=customer)
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()
			return redirect('user-profile')
	context = {'form':form, 'img':img , 'services':services , 'bookings' : bookings}
	return render(request, 'template/user.html',context)



