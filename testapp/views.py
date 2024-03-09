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
from datetime import datetime,timedelta
from urllib.parse import unquote
from django.db.models import Count, F, ExpressionWrapper, DateTimeField
from django.db.models.functions import Extract

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
tra=transaction.objects.filter(transaction_state='incoming')
for alll in tra:
    try:
        transaction_list= list(map(float, alll.transaction_data.split(',')))
        input_data = np.array(transaction_list)
        reshaped_data = input_data.reshape(1, -1)
    except:
        pass
    try:
        done=prediction(reshaped_data)
    except Exception as e:
        alll.transaction_state='invalid data'
        alll.save()
        
    
    newid=alll.transactionid
    if done==0:
        pred='legitimate'
        alll.transaction_state='predicted'
        alll.save()
        
    elif done==1:
        pred='fraud'
        transactlocation=alll.location
        try:
            userd=CustomUser.objects.get(location=transactlocation, department='agent')
            mystaffid = userd.staffid
            new_entry = alert.objects.create( transactionid=alll.transactionid,
                                            staffid=mystaffid, alert_status='waiting')
            new_entry.save()
            alll.transaction_state='predicted'
            alll.save()
        except:
            pass

all_stations=['Kiambu01','Kiambu02','Online01','Thika01','Thika02','Online02']
all_locations=['Kiambu','Thika','Online']  

def locator(request):
    try:
        user = request.user

        if user.is_authenticated:
            if user.department == 'agent' or user.department == 'manager':
                staff_location = user.location
                staff_station = [loc for loc in all_stations if re.match(f'^{re.escape(staff_location)}', loc)]
                
            elif user.department in ['support staff', 'admin']:
                # Support staff and admin see alerts from all locations
                staff_location = all_locations
                staff_station = all_stations

            content = {'staff_locations': staff_location, 'staff_stations': staff_station}
            return content
    except Exception as e:
        return HttpResponse(f'Error: {e}')

    return HttpResponse('User not logged in')     
global_data={}


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
        if data.get('location') not in all_stations:
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


@login_required
def home(request):
    
    user = request.user
    name=user.username
    
    if user.is_authenticated:
        content={'set':name}
        message='Welcome to Imara.'
    
    filter_stations=locator(request).get('staff_stations')

    
    current_date = datetime.now()
    # Calculate the date 5 years ago
    five_years_ago = current_date - timedelta(days=365 * 5)
    custom_start_date = five_years_ago.strftime("%Y-%m-%d")
    custom_end_date=current_date.strftime("%Y-%m-%d")
    time_view=[custom_start_date,' to ',custom_end_date]
    filter_transactions = transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
         
    all_transactions=transaction.objects.filter(timestamp__range=[custom_start_date, custom_end_date ],location__in=locator(request).get('staff_stations')).count()
    predicted=transaction.objects.filter(transaction_state='predicted',timestamp__range=[custom_start_date, custom_end_date ],location__in=locator(request).get('staff_stations')).count()
    pending=all_transactions-predicted
    all_alerts=alert.objects.filter(timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
    rejected=alert.objects.filter(alert_status='rejected',timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
    approved=alert.objects.filter(alert_status='approved',timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
    
    data = transaction.objects.filter(location__in= locator(request).get('staff_stations'),timestamp__range=[custom_start_date, custom_end_date ]).annotate(hour=Extract('timestamp','hour')).values('hour').annotate(count=Count('transactionid')).order_by('hour')
   
    try:
        approval_rate=int((approved/(approved+rejected))*100)
        
    except:
        approval_rate=0
        
    waiting=alert.objects.filter(alert_status='waiting',timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
    all_reports=report.objects.filter(timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
    false_positives=report.objects.filter(timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions,report_status='false positive').count()
    false_negatives=report.objects.filter(report_status='false negative',timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
    general_stats={'all_transactions':all_transactions,'transactions_per_hour':list(data),'predicted_transactions':predicted,'pending_transactions':pending,'all_alerts':all_alerts,'approved':approved,
        'rejected':rejected,'approval_rate':approval_rate,'waiting':waiting,'all_reports':all_reports,'false_positives':false_positives,
        'false_negatives':false_negatives,'locations':locator(request).get('staff_locations'),'stations':locator(request).get('staff_stations'),'time_view':time_view}
    context={'content':content,'general_stats':general_stats}
    filter_new_alerts = transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
    new_alerts=alert.objects.filter(alert_status='waiting',transactionid__in=filter_new_alerts).count()
    global_data['new_alerts']=new_alerts
    context['new_alerts']=new_alerts

    if request.method == 'POST':
        
        custom_start_date = request.POST.get('custom_start_date', '')
        custom_end_date = request.POST.get('custom_end_date', '')
        time_view=[custom_start_date,' to ',custom_end_date]
        custom_time_option = request.POST.get('customTimeOptions', '')
        filter_stations = request.POST.getlist('stations')
        
        if len(filter_stations)==0:
        
            filter_stations=locator(request).get('staff_stations')
    

        filter_transactions = transaction.objects.filter(location__in=[loc for loc in filter_stations if loc in locator(request).get('staff_stations')]).values_list('transactionid',flat=True)
              
        all_transactions=transaction.objects.filter(timestamp__range=[custom_start_date, custom_end_date ],location__in=[loc for loc in filter_stations if loc in locator(request).get('staff_stations')]).count()
        predicted=transaction.objects.filter(transaction_state='predicted',timestamp__range=[custom_start_date, custom_end_date ],location__in=[loc for loc in filter_stations if loc in locator(request).get('staff_stations')]).count()
        pending=all_transactions-predicted
        all_alerts=alert.objects.filter(timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
        rejected=alert.objects.filter(alert_status='rejected',timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
        approved=alert.objects.filter(alert_status='approved',timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
        
        data = transaction.objects.filter(location__in=[loc for loc in filter_stations if loc in locator(request).get('staff_stations')],timestamp__range=[custom_start_date, custom_end_date ]).annotate(hour=Extract('timestamp','hour')).values('hour').annotate(count=Count('transactionid')).order_by('hour')
    
        try:
            approval_rate=int((approved/(approved+rejected))*100)
            
        except:
            approval_rate=0
        waiting=alert.objects.filter(alert_status='waiting',timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
        all_reports=report.objects.filter(timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions).count()
        false_positives=report.objects.filter(timestamp__range=[custom_start_date, custom_end_date  ],transactionid__in=filter_transactions,report_status='false positive').count()
        false_negatives=report.objects.filter(report_status='false negative',timestamp__range=[custom_start_date, custom_end_date],transactionid__in=filter_transactions).count()
        
        general_stats={'all_transactions':all_transactions,'transactions_per_hour':list(data),'predicted_transactions':predicted,'pending_transactions':pending,'all_alerts':all_alerts,'approved':approved,
            'rejected':rejected,'approval_rate':approval_rate,'waiting':waiting,'all_reports':all_reports,
            'false_positives':false_positives,'false_negatives':false_negatives,'locations': locator(request).get('staff_locations'),'stations': locator(request).get('staff_stations'),
            'filtered_stations':[loc for loc in filter_stations if loc in locator(request).get('staff_stations')],'time_view':time_view}
        context={'content':content,'general_stats':general_stats,'login':message}
        filter_new_alerts = transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
        new_alerts=alert.objects.filter(alert_status='waiting',transactionid__in=filter_new_alerts).count()
        global_data['new_alerts']=new_alerts
        context['new_alerts']=new_alerts
        
        return render(request, 'homepage.html',context)
    else:
        pass
    
    return render(request, 'homepage.html',context)

  
@login_required
def alerts(request):

   
    user = request.user
    name=user.username
    if user.is_authenticated:
        content={'set':name}
    staff_location=locator(request).get('staff_stations')
    
   
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
        set_alert=f"Pending alerts:{count}"
        statement={'set':set_alert}
            
    else:
        set_alert='No pending alerts'
        statement={'set':set_alert}
    context={'set':alertpage,'content':content,'statement':statement,'count':count}
    filter_new_alerts = transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
    new_alerts=alert.objects.filter(alert_status='waiting',transactionid__in=filter_new_alerts).count()
    global_data['new_alerts']=new_alerts
    context['new_alerts']=new_alerts
    return render(request,'alertpage.html',context) 

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

    user = request.user
    name=user.username
    if user.is_authenticated:
        content={'set':name}
    
    filter_new_reports=transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
    filter_reports=report.objects.filter(transactionid__in=filter_new_reports,verification='waiting')
    entry_count = filter_reports.count()
    current_date = datetime.now()
    five_years_ago = current_date - timedelta(days=365 * 5)
    custom_start_date = five_years_ago.strftime("%Y-%m-%d")
    custom_end_date=current_date.strftime("%Y-%m-%d")
    time_view=[custom_start_date,' to ',custom_end_date]

    if request.method == 'POST':
        
        
        action=request.POST.get('action')
        report_transactionid = request.POST.get('transactionid')
        filter_reportid=request.POST.get('reportid')
        report_staffid=request.POST.get('staffid')
        reportstatus = request.POST.get('report_status')
        custom_start_date = request.POST.get('custom_start_date', '')
        custom_end_date = request.POST.get('custom_end_date', '')
        report_verification=request.POST.get('verification')
        time_view=[custom_start_date,' to ',custom_end_date]

        if action=='submit':
            
            new_entry = report.objects.create(transactionid=report_transactionid,
            staffid=user.staffid, report_status=reportstatus, verification='waiting')
            new_entry.save()
            if reportstatus=='false negative':   
                    new_entry = blacklist.objects.create(transactionid=report_transactionid,
                            category='false negative')
                    new_entry.save()

        if action=='update':
            items=request.POST.get('item_value')
            items=items.split(';')
            reportid=items[0].split(':')
            myreportid=reportid[1]
            selected=report.objects.get(reportid=myreportid)
            transactionid=report_transactionid
            staffid=report_staffid
            report_status=reportstatus 
            verification=report_verification
            change={'transactionid':transactionid,'staffid':staffid,'report_status': report_status,'verification':verification}
            for key, value in change.items():
                if value is not None:
                    setattr(selected, key, value)

        if action=='verify':
            items=request.POST.get('item_value')
            items=items.split(';')
            reportid=items[0].split(':')
            myreportid=reportid[1]
            selected=report.objects.get(reportid=myreportid)
            selected.verification='approved'
            selected.save()

        if action=='delete report':
            items=request.POST.get('item_value')
            items=items.split(';')
            reportid=items[0].split(':')
            myreportid=reportid[1]
            delete = get_object_or_404(report, reportid=myreportid)
            delete.delete()

        if action=='filter':
            filter_new_reports=transaction.objects.filter(
                location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
            filter_reports=report.objects.filter(timestamp__range=[custom_start_date, custom_end_date ],
            report_status=reportstatus,transactionid=report_transactionid,transactionid__in=filter_new_reports,
            reportid=filter_reportid,staffid=report_staffid,verification=report_verification)
    
    for all in filter_reports.values():
        if all['verification']=='waiting':
            waiting=True

    context={'filter':filter_reports,'content':content,'count':entry_count,'waiting':waiting,'time_view':time_view}

    filter_new_alerts = transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
    new_alerts=alert.objects.filter(alert_status='waiting',transactionid__in=filter_new_alerts).count()
    global_data['new_alerts']=new_alerts
    context['new_alerts']=new_alerts

    if user.is_staff == True:
        context['allowed']=True
    
    return render(request, 'reportspage.html',context)

@login_required
def blacklists(request):
 
    
    user = request.user
    name=user.username
    if user.is_authenticated:
        content={'set':name}

    full_list=blacklist.objects.all()

    count=full_list.count()
  
    if count>0:
         context={'set':full_list,'content':content}

    if request.method == 'POST':
        action=request.POST.get('action')
        
        if action=='remove':
            items=request.POST.get('item_value')
            items=items.split(';')
            listid=items[0].split(':')
            mylistid=listid[1]
            delete = get_object_or_404(blacklist, blacklistid=mylistid)
            delete.delete()
    filter_new_alerts = transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
    new_alerts=alert.objects.filter(alert_status='waiting',transactionid__in=filter_new_alerts).count()
    global_data['new_alerts']=new_alerts
    context['new_alerts']=new_alerts
    
    return render(request,'blacklist.html',context)

@login_required
def system(request):
  
    
    user = request.user
    name=user.username
    if user.is_authenticated:
        content={'set':name}
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
    filter_new_alerts = transaction.objects.filter(location__in= locator(request).get('staff_stations')).values_list('transactionid',flat=True)
    new_alerts=alert.objects.filter(alert_status='waiting',transactionid__in=filter_new_alerts).count()
    global_data['new_alerts']=new_alerts
    content['new_alerts']=new_alerts
    return render(request, 'modelpage.html',content)

@login_required
def guidelines(request):
    user = request.user
    name=user.username
    if user.is_authenticated:
        content={'set':name}
    return render(request,'guidelines.html',content)

def logout_view(request):
    logout(request)
   
    return redirect(home)
