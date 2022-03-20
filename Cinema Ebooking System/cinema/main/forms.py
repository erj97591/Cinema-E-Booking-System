from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=200)
	phone_number = forms.IntegerField()
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	street = forms.CharField(max_length=200)
	city = forms.CharField(max_length=300)
	state = forms.CharField(max_length=2)
	zip_code = forms.CharField()
	card_number = forms.IntegerField()
	ccv = forms.IntegerField()
	expiration_date = forms.DateField()

	class Meta:
		model = User
		fields = ["username","first_name", "last_name",  "email", "password1", "password2", "street", "city", "state", "zip_code", "card_number", "ccv", "expiration_date"]