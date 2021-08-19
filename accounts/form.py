from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
# from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib import messages


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class settigs_form(ModelForm):
    Birthday = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    proof = forms.ImageField(widget=forms.FileInput)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_messages={
        'required': "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."})

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'Gender', 'Birthday', 'phone_number', 'address1', 'address2', 'pin_code', 'city',
                  'country', 'proof']


class update_profile_form(ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = CustomUser
        fields = ['profile_pic']


class passwordchangingform(PasswordChangeForm):
    old_password = forms.CharField(max_length=50,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=50,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=50,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']
