from django import forms
from django.contrib.auth.forms import AuthenticationForm
class loginform(AuthenticationForm):
    username=AuthenticationForm()
    password=AuthenticationForm()
