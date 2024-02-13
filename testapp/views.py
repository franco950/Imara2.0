from django.http import HttpResponse 
from django.shortcuts import render, redirect,get_object_or_404
from testapp.models import transaction,alert,report,blacklist,systemsettings
import pandas as pd
import numpy as np
import joblib 
from testapp.predictor import always
import ast
from .forms import SearchForm,SystemSettingsForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

loaded_model = joblib.load('trained_model.joblib')

def prediction(data):
    return loaded_model.predict(data)


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
    alertsettings=systemsettings.objects.create(settings_class='alert')
    alertsettings.save()
    reportgen=systemsettings.objects.all()
    automate=reportgen.values()
    swe=[]
    
    incoming = transaction.objects.filter(transaction_state='incoming')
    datas=incoming.values()
    
    for tems in datas:
    
        transaction_list=[]
        neww=tems['transaction_data']    
        neww=neww.split(',')
        for num in neww:
            num=float(num)
            transaction_list.append(num) 

        input_data = np.array(transaction_list)
        my = input_data.reshape(1, -1)
        done=prediction(my)
        new=transaction.objects.get(transactionid=(tems['transactionid']))
        if done==0:
            new.transaction_state='predicted'
            new.save()
    
        if done==1:
            user = request.user
            mystaffid = user.staffid
            new_entry = alert.objects.create( transactionid=tems['transactionid'],staffid=mystaffid, alert_status='waiting')
            new_entry.save()
            new.transaction_state='predicted'
            new.save()
            
    incoming.update(transaction_state="predicted")
    alertpage=alert.objects.filter(alert_status='waiting')
    fraudalerts=alertpage.values()
    entry_count = alertpage.count()

    if entry_count==0:
        
        content={'set':'no alerts here'}
    else:
    
        for all in fraudalerts:
           
            swe.append(all)
    
    if request.method == 'POST':

        item_value = request.POST.get('item_value')
        action = request.POST.get('action')
        data = ast.literal_eval(item_value)
        if action=='reject':
            new_entry = blacklist.objects.create(transactionid=data.get('transactionid'),
             category='true positive')
            new_entry.save()

        if action=='approve':
            new_entry = report.objects.create(transactionid=data.get('transactionid'),
               staffid=data.get('staffid'), report_status='false positive',verification='waiting')
            new_entry.save()
        alertchange=alert.objects.get(alertid=data.get('alertid'))
        alertchange.alert_status = 'handled'
        alertchange.save()
            
        for all in swe:
            x=all['alertid']
            y=data.get('alertid')
            if x==y:
                all['alert_status']='handled'
  
    swe = [item for item in swe if item['alert_status'] != 'handled']
    transactlist=[]
    user = request.user
    if user.is_authenticated:
       

        staff_location = user.location
        
        transactions = transaction.objects.filter(location=staff_location)
        transactionvalues=transactions.values()
        for all in transactionvalues:
            
            transactlist.append(all)
      

    new = [dict1 for dict1 in swe for dict2 in transactlist if int(dict1['transactionid']) == dict2['transactionid']]

    content={'set':new}
            
    return render(request,'alertpage.html',content)     
@login_required
def reports(request):
    settings=systemsettings.objects.get(settings_class='general')
    
    reportlist=[]
    reportspage=report.objects.filter(verification='waiting')
    reportvalues=reportspage.values()
    entry_count = reportspage.count()
    if entry_count==0:
        content={'set':'no reports here'}
    else:
        for all in reportvalues:
            reportlist.append(all)

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
                if settings.blacklist_add=='false negatives':
                    print(39)
                
                    new_entry = blacklist.objects.create(transactionid=report_transactionid,
                            category='false negative')
                    new_entry.save()
                else:
                    print(40)
        
        if action=='delete report':
            items=request.POST.get('item_value')
            data = ast.literal_eval(items)
            deletereport = get_object_or_404(report, reportid=data.get('reportid'))
            deletereport.delete()
            for all in reportlist:
                x=all['reportid']
                y=data.get('reportid')
                if x==y:
                    reportlist.remove(all)
    content={'set':reportlist}
    return render(request, 'reportspage.html',content)

@login_required
def blacklists(request):
    blacklistfull=[]
    true_positives=[]
    false_negatives=[]
    full_list=blacklist.objects.all()
    full_listvalues=full_list.values()
    count=full_list.count()
    
  
    if count>0:
        for all in full_listvalues:
            blacklistfull.append(all)
    # if request.method=='GET':
    #     search_query = request.GET.get('search_query', '')
    #     queryset = blacklist.objects.filter(name__icontains=search_query)

    if request.method == 'POST':
        action=request.POST.get('action')
        
        
        if action=='remove':
            items=request.POST.get('item_value')
            data = ast.literal_eval(items)
            delete = get_object_or_404(blacklist, blacklistid=data.get('blacklistid'))
            delete.delete()
            for all in blacklistfull:
                x=all['blacklistid']
                y=data.get('blacklistid')
                if x==y:
                    blacklistfull.remove(all)
    
        
      
    true_positives=[item for item in blacklistfull if item['category'] =='true positive']
    false_negatives=[item for item in blacklistfull if item['category'] =='false negative']
     
   # content = {'set':blacklistfull,'queryset': queryset, 'search_form': SearchForm(initial={'search_query': search_query})}
    
    content={'set':blacklistfull}
    
   

    return render(request,'blacklist.html',content)

@login_required
def system(request):
    settings,created=systemsettings.objects.get_or_create(settings_class='general')
    
   
   
  
    if request.method == 'POST':
        
        form = SystemSettingsForm(request.POST)
        if form.is_valid():
            settings.automate = form.cleaned_data.get('automate')
            settings.locations = form.cleaned_data.get('locations')
            settings.blacklist_add = form.cleaned_data.get('blacklist_add')
            settings.report_add = form.cleaned_data.get('report_add')
            settings.enforce_blacklist = form.cleaned_data.get('enforce_blacklist')
            settings.save()
            
            #return redirect(system)
    else:
        form = SystemSettingsForm(
            initial={
            'automate': settings.automate,
            'locations': settings.locations,
            'blacklist_add': settings.blacklist_add,
            'report_add': settings.report_add,
            'enforce_blacklist': settings.enforce_blacklist}
        )
    context={'form':form}
    return render(request,'modelpage.html',context)



   

@login_required
def guidelines(request):
    return render(request,'guidelines.html')


def logout_view(request):
    logout(request)
   
    return redirect(home)


