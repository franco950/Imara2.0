from django.http import HttpResponse 
from .forms import loginform
from testapp.views import home
from .models  import staff_member
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login


def loginpage(request):
    if request.method == 'POST':
        form = loginform(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(home)
    else:
        form = loginform()
    return render(request, 'login.html', {'form': form})

