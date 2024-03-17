from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone  
from django.core.validators import MinValueValidator, MaxValueValidator
class CustomUser(AbstractUser):
    staffid = models.IntegerField(max_length=10, blank=True, null=True,unique=True,  validators=[MinValueValidator(1000), MaxValueValidator(10000000)])
    department=models.CharField(max_length=30)
    location=models.CharField(max_length=20)
    def __str__(self):
        return f"{str(self.staffid)}  :  {self.username} :  {self.department}  : {self.location}: {self.email}"
    
class transaction(models.Model):
    transactionid=models.AutoField(primary_key=True)
    location=models.CharField(max_length=30)
    transaction_data=models.CharField(max_length=3000)
    transaction_state=models.CharField(max_length=11, default='incoming')
    timestamp = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))
    def __str__(self):
        return f"{str(self.transactionid)} : {self.location} : {self.transaction_state}"
       
class alert(models.Model):
    alertid=models.AutoField( primary_key=True)
    transactionid=models.CharField(max_length=20)
    staffid=models.CharField(max_length=30)
    alert_status=models.CharField(max_length=30)
    timestamp = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))
  
    def __str__(self):
        return f"alert id:{str(self.alertid)}  ; transaction id:  {self.transactionid} ; staff id: {self.staffid} ; alert status: {self.alert_status}"
       
class report(models.Model):
    reportid=models.AutoField(primary_key=True)
    transactionid=models.CharField(max_length=20)
    staffid=models.CharField(max_length=40)
    report_status=models.CharField(max_length=30)
    verification=models.CharField(max_length=30 )
    timestamp = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))
  
    def __str__(self):
        return f"report id:{str(self.reportid)}  ; transaction id: {self.transactionid} ; staff id: {self.staffid} ; report status: {self.report_status} ; verification: {self.verification}"
        
class blacklist(models.Model):
    blacklistid=models.IntegerField(primary_key=True)
    transactionid=models.CharField(max_length=20)
    category=models.CharField(max_length=30)

    def __str__(self):
        return f"blacklist id:{str(self.blacklistid)}  ;  transaction id: {self.transactionid} ; category: {self.category }"

class systemsettings(models.Model):
    settings_class=models.CharField( max_length=20, default='general')
    locations=models.CharField( max_length=50, default='none')
    stations=models.CharField( max_length=50, default='none')
    automate=models.CharField( max_length=100, default='none')
    enforce_blacklist=models.BooleanField(default=False)
    blacklist_add=models.CharField( max_length=100,default='none')
    report_add=models.CharField( max_length=100, default='none')

    def __str__(self):
        return f"{str(self.settings_class)}  : {self.automate} : {self.locations} : {self.stations} :  {self.enforce_blacklist} : {self.blacklist_add} : {self.report_add}"