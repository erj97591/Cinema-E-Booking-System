from django import forms
from django.forms import ModelForm
from .models import PaymentCard, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    phone_number = forms.IntegerField(help_text='Phone')
    address = forms.CharField(max_length=500, help_text='Address')
    promotions = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'phone_number', 'address', 'promotions')



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'promotions')


class PaymentForm(ModelForm):

    class Meta:
        model = PaymentCard
        fields = ['card_number', 'expiration_date', ]

