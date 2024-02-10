from django.http import HttpResponse 
from .forms import loginform,resetform
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
def reset(request):
    if request.method=='POST':
        form = resetform(request,request.GET)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = authenticate(request, username=username)
            if user is not None:
                return HttpResponse('wait for a reset password')
    else:
        form=resetform()
    return render(request, 'resetpage.html',{'form': form} )
# def password_reset_confirm(request):
    
#     user_uidb64 = '...'  # Replace with the actual uidb64 value for the user
#     user_token = '...'   # Replace with the actual token value for the user

#     context = {
#         'user_uidb64': user_uidb64,
#         'user_token': user_token,
#     }

#     return render(request, 'password_reset_confirm.html', context)