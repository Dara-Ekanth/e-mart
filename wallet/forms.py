from .models import *
from django.forms import ModelForm
from django import forms
from .views import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class reg_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class bill_form(ModelForm):
#     class Meta:
#         model = bill
#         fields = ['name', 'amount', 'email']


class wallet_form(ModelForm):
    class Meta:
        model = wallet
        fields = ['balance']
