from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Report_item



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','username','email','password1','password2')




class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','password1')