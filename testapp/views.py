from django.http import HttpResponse 
from django.shortcuts import render, redirect,get_object_or_404
from testapp.models import transaction,alert,report,blacklist,systemsettings,CustomUser
import pandas as pd
import numpy as np
import joblib 
from testapp.predictor import always
from .forms import SearchForm,SystemSettingsForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework import status,generics
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
loaded_model = joblib.load('trained_model smote.joblib')

def prediction(data):
    return loaded_model.predict(data)

locations=['Kiambu01','Kiambu02','Online01','Thika01','Thika02','Online02']
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transactions(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            # Handle invalid JSON in the request
            return JsonResponse({'error': 'Invalid JSON in the request'}, status=400)
            
        # Process the data or save it to the database
        newentry=transaction.objects.create(location=data.get('location'), transaction_data=data.get('data'))
        newentry.save()
        if data.get('location') not in locations:
            newentry.transaction_state='invalid location'
            newentry.save()
            return JsonResponse({"error":"invalid transaction location"})


        transaction_list=[]
        neww=newentry.transaction_data    
        neww=neww.split(',')
        for num in neww:
            transaction_list.append(float(num)) 

        input_data = np.array(transaction_list)
        reshaped_data = input_data.reshape(1, -1)
                
        try:
            done=prediction(reshaped_data)
        except:
            newentry.transaction_state='invalid data'
            newentry.save()
            return JsonResponse({"error":"invalid transaction data"})
        
        newid=newentry.transactionid
        if done==0:
            pred='legitimate'
            newentry.transaction_state='predicted'
            newentry.save()
            
        elif done==1:
            pred='fraud'
            transactlocation=newentry.location
            userd=CustomUser.objects.get(location=transactlocation, department='agent')
            
            mystaffid = userd.staffid
            
            new_entry = alert.objects.create( transactionid=newentry.transactionid,
                                                staffid=mystaffid, alert_status='waiting')
            new_entry.save()
            newentry.transaction_state='predicted'
            newentry.save()
        
            # Respond with a JSON success message
        return JsonResponse({'message': 'Data received successfully','transaction id' :str(newid),
                            'prediction':str(pred),'mode':'manual'})
        
        
def home(request):
    user = request.user
    name=user.username
    if user.is_authenticated:
        content={'set':name}
        return render(request, 'homepage.html',content)
    else: 
        return render(request, 'homepage.html')
  
@login_required
def alerts(request):
    
    user = request.user
    if user.is_authenticated:
        if user.department=='agent':
            staff_location = user.location
        elif user.department=='manager':
            area=user.location
            staff_location = [loc for loc in locations if re.match(f'^{re.escape(area)}', loc)]
            
        else:
            #support staff and admin see alerts from all locations
            staff_location=locations
   
    if request.method == 'POST':

        items = request.POST.get('item_value')
        action = request.POST.get('action')
        items=items.split(';')
        alertid=items[0].split(':')
        myalertid=alertid[1]
        alertchange=alert.objects.get(alertid=myalertid)  

        if action=='reject':
            
            alertchange.alert_status='rejected'
            alertchange.save()
            new_entry = blacklist.objects.create(transactionid=alertchange.transactionid,
            category='true positive')
            new_entry.save()

        if action=='approve':
            alertchange.alert_status='approved'
            alertchange.save()
            new_entry = report.objects.create(transactionid=alertchange.transactionid,
            staffid=alertchange.staffid, report_status='false positive',verification='waiting')
            new_entry.save()
    
    transactions = transaction.objects.filter(location__in=staff_location).values_list('transactionid',flat=True)
    alertpage=alert.objects.filter(alert_status='waiting',transactionid__in=transactions)
    count = alertpage.count()

    if count>0:
        
        content={'set':alertpage}
        return render(request,'alertpage.html',content)    
    else:
        return render(request,'alertpage.html') 

@api_view(['GET'])   
@permission_classes([IsAuthenticated])
def feedback(request):
     if request.method=='GET':
        try:
            data = json.loads(request.body.decode('utf-8'))
            identity=data.get('transaction id')
        except json.JSONDecodeError:
            # Handle invalid JSON in the request
            return JsonResponse({'error': 'Invalid JSON in the request'}, status=400)
        try:
            alertreturn=alert.objects.get(transactionid=identity)
        except:
            return JsonResponse({'error': 'Transaction id not found'})
        staff_member=alertreturn.staffid
        alert_id= alertreturn.alertid
        alert_status=alertreturn.alert_status
        return JsonResponse({'message': 'Data retrieved successfully','transaction id' :str(identity),
        'alert id' : str(alert_id),'staff id' : str(staff_member), 'alert status' : str(alert_status)})
  
@login_required
def reports(request):

    if request.method == 'POST':
        user=request.user
        action=request.POST.get('action')
        report_transactionid = request.POST.get('transactionid')
        reportstatus = request.POST.get('report_status')
        if action=='submit':
    
            new_entry = report.objects.create(transactionid=report_transactionid,
            staffid=user.staffid, report_status=reportstatus, verification='waiting')
            new_entry.save()
            if reportstatus=='false negative':   
                    new_entry = blacklist.objects.create(transactionid=report_transactionid,
                            category='false negative')
                    new_entry.save()

        if action=='delete report':
            items=request.POST.get('item_value')
            items=items.split(';')
            reportid=items[0].split(':')
            myreportid=reportid[1]
            delete = get_object_or_404(report, reportid=myreportid)
            delete.delete()
    reportspage=report.objects.filter(verification='waiting')
   
    entry_count = reportspage.count()
    if entry_count>0:
        context={'set':reportspage}
    else:
        return render(request, 'reportspage.html')
            
    return render(request, 'reportspage.html',context)

@login_required
def blacklists(request):

    full_list=blacklist.objects.all()

    count=full_list.count()
  
    if count>0:
         content={'set':full_list}

    if request.method == 'POST':
        action=request.POST.get('action')
        
        if action=='remove':
            items=request.POST.get('item_value')
            items=items.split(';')
            listid=items[0].split(':')
            mylistid=listid[1]
            delete = get_object_or_404(blacklist, blacklistid=mylistid)
            delete.delete()
    
    return render(request,'blacklist.html',content)

@login_required
def system(request):
    settings,created=systemsettings.objects.get_or_create(settings_class='general')
    form=SystemSettingsForm()
   
    if request.method == 'POST':
        
        form = SystemSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            # settings.automate = form.cleaned_data.get('automate')
            # settings.locations = form.cleaned_data.get('locations')
            # settings.blacklist_add = form.cleaned_data.get('blacklist_add')
            # settings.report_add = form.cleaned_data.get('report_add')
            # settings.enforce_blacklist = form.cleaned_data.get('enforce_blacklist')
            # settings.save()
            
            #return redirect(system)
    # else:
    #     form = SystemSettingsForm(
    #         initial={
    #         'automate': settings.automate,
    #         'locations': settings.locations,
    #         'blacklist_add': settings.blacklist_add,
    #         'report_add': settings.report_add,
    #         'enforce_blacklist': settings.enforce_blacklist}
    #     )
    context={'form':form}
    return render(request,'modelpage.html',context) 

@login_required
def guidelines(request):
    return render(request,'guidelines.html')

def logout_view(request):
    logout(request)
   
    return redirect(home)
