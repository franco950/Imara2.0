"""
URL configuration for testproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from testapp.views import home,transactions,alerts,reports,system,guidelines,blacklists,logout_view,feedback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', include('login.urls')),
    path('',home,name='home'),
    path('transactions',transactions,name='transactions'),
    path('alerts',alerts,name='alerts'),
    path('feedback',feedback,name='feedback'),
    path('reports',reports,name='reports'),
    path('blacklist',blacklists,name='blacklist'),
    path('model',system,name='model'),
    path('guidelines',guidelines,name='guidelines'),
     path('logout/', logout_view, name='logout'),
   # path('testapp', include('testapp.urls', namespace='testapp')),
    

]