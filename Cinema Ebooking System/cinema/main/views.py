from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
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
def registration(response):
	return render(response, "main/registrationpage.html")
