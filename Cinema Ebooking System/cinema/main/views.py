from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, User
from . import views 
from .forms import RegistrationForm

# Create your views here.
def home(response, id):
	if id == 2:
		return render(response, "main/homepage2.html", {})
	else: return render(response, "main/homepage1.html",{})
def login_page(response):
	if response.method=="POST":
		email = response.POST['username']
		password = response.POST['password']
		
	return render(response, "main/loginpage.html")
def seat_view(response, id):
	if id ==2:
		return render(response, "main/seat.html", {})
	else: return render(response, "main/seats2.html",{})
def registration_page(response):
	form = RegistrationForm(response.POST)
	if form.is_valid():
		form.save()
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password1')
		user = authenticate(username=username, password=password)
		return redirect('main/homepage1.html')
	return render(response, "main/registration.html", {'form': form})
