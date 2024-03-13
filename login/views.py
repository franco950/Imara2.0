from django.http import HttpResponse 
from .forms import loginform
from testapp.views import home,alerts
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import cache_control

def loginpage(request):
    if request.method == 'POST':
        form = loginform(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            userd = authenticate(request, username=username, password=password)
            if userd is not None:
                login(request, userd)
                return redirect(alerts)
    else:
        form = loginform()
    return render(request, 'login.html', {'form': form})

