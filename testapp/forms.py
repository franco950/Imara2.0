from django import forms
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    is_active = forms.BooleanField(required=False)
    staffid = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        validate_password(password)
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        is_active = self.cleaned_data.get('is_active', False)
        staffid = self.cleaned_data['staffid']
        department = self.cleaned_data['department']
        location = self.cleaned_data['location']
        
        # Create user with validated password
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=is_active,
            staffid = staffid,
            department = department,
            location = location
        )
    
        
        user.save()
        return user