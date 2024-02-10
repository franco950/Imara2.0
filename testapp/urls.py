from django.urls import path
from django.contrib import admin
from .views import home,alerts,reports,modelpage,guidelines,blacklists

urlpatterns=[
    path('home',home,name='home'),
    path('alerts',alerts,name='alerts'),
    path('reports',reports,name='reports'),
    path('blacklist',blacklists,name='blacklist'),
    path('model',modelpage,name='model'),
    path('guidelines',guidelines,name='guidelines'),


]