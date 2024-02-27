from django.http import HttpResponse 
from django.shortcuts import render, redirect,get_object_or_404
from testapp.models import transaction,alert,report,blacklist,systemsettings,CustomUser
import numpy as np
import joblib 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
from rest_framework import status,generics
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.test import APIClient
import requests
import os
from datetime import datetime
from urllib.parse import unquote

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
directory_path = 'testapp\joblib models'
file_names = os.listdir(directory_path)

# Extract timestamps from file names
timestamps = [datetime.strptime(file_name.split('_')[1], '%Y%m%d%H%M%S') for file_name in file_names]

# Identify the file with the latest timestamp
latest_file_index = timestamps.index(max(timestamps))
latest_file = file_names[latest_file_index]
# Access or perform operations with the file having the latest timestamp
latest_file_path=f'testapp\\joblib models\\{latest_file}'
def getversion():
    client=APIClient()
    url = 'http://127.0.0.1:8001/version'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('version') == latest_file:
            print('System has the latest model version')

            return JsonResponse({'message': 'System has the latest model version'})
        else:
           
            # Request the joblib file
            request_joblib_file()

    else:
        print(f"API call failed with status code: {response.status_code}")
# Process the data based on a certain value
def extract_filename(content_disposition):
    if content_disposition:
        _, params = content_disposition.split(';', 1)
        for param in params.split(';'):
            key, value = param.strip().split('=')
            if key == 'filename':
                return unquote(value)
    return f'downloadedmodel_{timestamp}_.joblib'  # Default name if filename extraction fails      

def request_joblib_file():
    client=APIClient()
    joblib_url = 'http://127.0.0.1:8001/download'  # Replace with the actual URL for the joblib file
    joblib_response = requests.get(joblib_url)

    if joblib_response.status_code == 200:
        content_disposition = joblib_response.headers.get('Content-Disposition')
        print(content_disposition)
        filename = extract_filename(content_disposition)
         
        if filename:
            # Save the joblib file locally or process it as needed
            with open(f'testapp\\joblib models\\{filename}', 'wb') as f:
                f.write(joblib_response.content)
            print("Joblib file downloaded successfully.")
        else:
            print("Failed to extract filename from Content-Disposition header.")
        
    else:
        print(f"Failed to download joblib file with status code: {joblib_response.status_code}")


# Make the API call
try:
    getversion()
except Exception:
    ("error problem accessing the machine learning system")

try:
    loaded_model = joblib.load(latest_file_path)
except:
    Exception("problem........... ")

def prediction(data):
    return loaded_model.predict(data)

locations=['Kiambu01','Kiambu02','Online01','Thika01','Thika02','Online02']
regions=['Kiambu','Thika','Online']
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transactions(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            # Handle invalid JSON in the request
            return JsonResponse({'error': 'Invalid JSON in the request'}, status=400)
            
        # Process the data and save it to the database
        newentry=transaction.objects.create(location=data.get('location'), transaction_data=data.get('data'))
        newentry.save()
        if data.get('location') not in locations:
            newentry.transaction_state='invalid location'
            newentry.save()
            return JsonResponse({"error":"invalid transaction location"})

        transaction_list= list(map(float, newentry.transaction_data.split(',')))
        input_data = np.array(transaction_list)
        reshaped_data = input_data.reshape(1, -1)
                
        try:
            done=prediction(reshaped_data)
        except Exception as e:
            newentry.transaction_state='invalid data'
            newentry.save()
            return JsonResponse({"error":f"invalid transaction data {str(e)}"})
        
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
    else:
        content={'set':'guest'}
    all_transactions=transaction.objects.all().count()
    all_alerts=alert.objects.all().count()
    rejected=alert.objects.filter(alert_status='rejected').count()
    approved=alert.objects.filter(alert_status='approved').count()
    print(approved)
    try:
        approval_rate=(approved/all_alerts)*100
        print(approval_rate)
    except:
        pass
    waiting=alert.objects.filter(alert_status='waiting').count()
    all_reports=report.objects.all().count()
    false_positives=report.objects.filter(report_status='false positive').count()
    false_negatives=report.objects.filter(report_status='false negative').count()
    general_stats={'all_transactions':all_transactions,'all_alerts':all_alerts,'approved':approved,
        'rejected':rejected,'approval_rate':approval_rate,'waiting':waiting,'all_reports':all_reports,
        'false_positives':false_positives,'false_negatives':false_negatives}
    if request.method == 'POST':
        print('yaaaaaay')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        region=request.POST.get('location')
        location=request.POST.get('station')
        specify=request.POST.get('specify')
        status=request.POST.get('status')
       
    
        def get_region(region,start,end,status):
            start=request.POST.get('start_date')
            end = request.POST.get('end_date')
            region=request.POST.get('location')
            loca=request.POST.get('station')
            specify=request.POST.get('specify')
            status=request.POST.get('status')
            
            areas = [loc for loc in locations if re.match(f'^{re.escape(region)}', loc)]
            transactions = transaction.objects.filter(location__in=areas).values_list('transactionid',flat=True)
            get_alert=alert.objects.filter(alert_status=[stat for stat in status if status],timestamp__range=[start, end ],transactionid__in=transactions).count()
            print(get_alert)
            return get_alert
        
        def get_station(loca,start,end,status):
            start=request.POST.get('start_date')
            end = request.POST.get('end_date')
            region=request.POST.get('location')
            loca=request.POST.get('station')
            specify=request.POST.get('specify')
            status=request.POST.get('status')
            transactions = transaction.objects.filter(location__in=loca).values_list('transactionid',flat=True)
            get_alert=alert.objects.filter(alert_status=[stat for stat in status if status],timestamp__range=[start, end],transactionid__in=transactions).count()
            return get_alert
        
        def get_map(specify,data):
            result={}
            if specify=='location':
                data=region
                for all in data:
                    result[all]=get_region()
            elif specify=='station':
                data=location
                for all in data:
                    result[all]=get_station()
            return result
        return HttpResponse('YAAAAY')
      #  filter_stats={'map':get_map(),'region':get_region(),'station':get_station()}
        
    
    
     
   
    # try:
    #     context={'content':content,'general_stats':general_stats,'filter_stats':filter_stats}
    #     return render(request, 'homepage.html',context)
    #except:
    else:
        print(general_stats)
        context={'content':content,'general_stats':general_stats}
        return render(request, 'homepage.html',context)
    
  
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
            return JsonResponse({'error': 'Transaction id not found, Check request structure'})
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
    settings = None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name == 'settings class':
            settings_class = request.POST.get('settings_class')
            
            if settings_class == 'general':
                settings, created = systemsettings.objects.get_or_create(settings_class='general')
            else:
                settings, created = systemsettings.objects.get_or_create(settings_class='specific')

        else:
            # Retrieve the existing settings or create a new instance if it doesn't exist
            settings, created = systemsettings.objects.get_or_create(settings_class='general')

            if name == 'location':
                locations = request.POST.get('location')
                settings.locations = locations
            elif name == 'station':
                stations = request.POST.getlist('station')  # Get a list of selected stations
                settings.stations = ",".join(stations)
            elif name == 'automate':
                automate = request.POST.get('automate')
                settings.automate = automate
            elif name == 'enforce':
                enforce = request.POST.get('enforce')
                settings.enforce_blacklist = True if enforce == 'enforce' else False
            elif name == 'blacklist_add':
                blacklist_add = request.POST.getlist('blacklist_add')  # Get a list of selected items
                settings.blacklist_add = ",".join(blacklist_add)
            elif name == 'report_add':
                report_add = request.POST.get('reports')
                settings.report_add = report_add

            # Save the instance after making changes
            settings.save()

    return render(request, 'modelpage.html')

   

@login_required
def guidelines(request):
    return render(request,'guidelines.html')

def logout_view(request):
    logout(request)
   
    return redirect(home)
