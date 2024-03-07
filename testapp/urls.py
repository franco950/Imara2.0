from django.urls import path
from django.contrib import admin
from . import views 

urlpatterns=[
    path('',views.home,name='home'),
    path('transactions',views.transactions,name='transactions'),
    path('alerts/',views.alerts,name='alerts'),
    path('feedback',views.feedback,name='feedback'),
    path('reports/',views.reports,name='reports'),
    path('blacklist/',views.blacklists,name='blacklist'),
    path('model/',views.system,name='model'),
    path('guidelines/',views.guidelines,name='guidelines'),
    path('logout/', views.logout_view, name='logout')
]