from django.urls import path
from django.contrib import admin
from .views import home,transactions,alerts,reports,system,guidelines,blacklists,logout_view

urlpatterns=[
    path('',home,name='home'),
    path('transactions',transactions,name='transactions'),
    path('alerts',alerts,name='alerts'),
    path('reports',reports,name='reports'),
    path('blacklist',blacklists,name='blacklist'),
    path('model',system,name='model'),
    path('guidelines',guidelines,name='guidelines'),
     path('logout/', logout_view, name='logout'),


]