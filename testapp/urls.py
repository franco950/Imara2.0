from django.urls import path
from django.contrib import admin
from . import views 

urlpatterns=[
    path('adminpanel/',views.adminpanel,name='adminpanel'),
    path('dashboard/',views.home,name='home'),
    path('transactions',views.transactions,name='transactions'),
    path('alerts/',views.alerts,name='alerts'),
    path('feedback',views.feedback,name='feedback'),
    path('reports/',views.reports,name='reports'),
    path('blacklists/',views.blacklists,name='blacklists'),
    path('model/',views.system,name='model'),
    path('logout/', views.logout_view, name='logout'),
    path('staff-report/', views.staff_report, name='staff_report'),
    path('false-report/', views.false_report, name='false_report'),
    path('alerts-report/', views.alerts_report, name='alerts_report'),
    path('transactions-report/', views.transactions_report, name='transactions_report'),
    path('blacklist-report/', views.blacklist_report, name='blacklist_report'),
]