from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone  
class CustomUser(AbstractUser):
    staffid = models.CharField(max_length=10, blank=True, null=True)
    department=models.CharField(max_length=30)
    location=models.CharField(max_length=20)
    def __str__(self):
        return f"{str(self.staffid)}  :  {self.username} :  {self.department}  : {self.location}"



class transaction(models.Model):
    transactionid=models.AutoField(primary_key=True)
    location=models.CharField(max_length=30)
    transaction_data=models.CharField(max_length=3000)
    transaction_state=models.CharField(max_length=11, default='incoming')
    timestamp = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return f"{str(self.transactionid)} : {self.location} : {self.transaction_state}"
       
class alert(models.Model):
    alertid=models.AutoField( primary_key=True)
    transactionid=models.CharField(max_length=20)
    staffid=models.CharField(max_length=30)
    alert_status=models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return f"alert id:{str(self.alertid)}  ; transaction id:  {self.transactionid} ; staff id: {self.staffid} ; alert status: {self.alert_status}"
       
class report(models.Model):
    reportid=models.AutoField(primary_key=True)
    transactionid=models.CharField(max_length=20)
    staffid=models.CharField(max_length=40)
    report_status=models.CharField(max_length=30)
    verification=models.CharField(max_length=30 )
    timestamp = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return f"report id:{str(self.reportid)}  ; transaction id: {self.transactionid} ; staff id: {self.staffid} ; report status: {self.report_status}"
        
class blacklist(models.Model):
    blacklistid=models.IntegerField(primary_key=True)
    transactionid=models.CharField(max_length=20)
    category=models.CharField(max_length=30)

    def __str__(self):
        return f"blacklist id:{str(self.blacklistid)}  ;  transaction id: {self.transactionid} ; category: {self.category }"

class systemsettings(models.Model):
    AUTOMATION = [
        ('all', 'Automate All Transactions'),
        ('location', 'automate by location'),
        ('off', 'no automation')
    ]
    LOCATIONS=[('none','none'),
               ('Kiambu01','Kiambu01'),
               ('Kiambu0','Kiambu02'),
               ('Thika01','Thika01'),
               ('Thika02','Thika02'),
               ('Online','Online')]
    BLACKLIST=[
               ('rejected alerts', 'add rejected alerts to the blacklist automatically'),
               ('false negatives','add false negatives to the blacklist automatically')]
    REPORT=[('auto', 'automatically generate reports from allowed transactions'),
            ('redirect','redirect the user to manually create a report after allowing a flagged transaction'),
            ('none', 'do not redirect the user or generate a report automatically')]


    settings_class=models.CharField( max_length=20, default='general')
    locations=models.CharField(choices=LOCATIONS, max_length=50, default='all')
    automate=models.CharField(choices=AUTOMATION, max_length=100, default='none')
    enforce_blacklist=models.BooleanField(default=False)
    blacklist_add=models.CharField(choices=BLACKLIST, max_length=100,default='rejected alerts')
    report_add=models.CharField(choices=REPORT, max_length=100, default='auto')

    def __str__(self):
        return f"{str(self.settings_class)}  : {self.automate} : {self.locations} :  {self.enforce_blacklist} : {self.blacklist_add} : {self.report_add}"