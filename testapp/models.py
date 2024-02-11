from django.db import models
from django.contrib.auth.models import AbstractUser

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
  
    def __str__(self):
        return f"{str(self.transactionid)} : {self.location} : {self.transaction_state}"
       
class alert(models.Model):
    alertid=models.AutoField( primary_key=True)
    transactionid=models.CharField(max_length=20)
    staffid=models.CharField(max_length=30)
    alert_status=models.CharField(max_length=30)
  
    def __str__(self):
        return f"{str(self.alertid)}  :  {self.transactionid} : {self.staffid} : {self.alert_status}"
       
class report(models.Model):
    reportid=models.AutoField(primary_key=True)
    transactionid=models.CharField(max_length=20)
    staffid=models.CharField(max_length=40)
    report_status=models.CharField(max_length=30)
    verification=models.CharField(max_length=30 )
  
    def __str__(self):
        return f"{str(self.reportid)}  :  {self.transactionid} : {self.staffid} : {self.report_status}"
        
class blacklist(models.Model):
    blacklistid=models.IntegerField(primary_key=True)
    transactionid=models.CharField(max_length=20)
    category=models.CharField(max_length=30)

    def __str__(self):
        return f"{str(self.blacklistid)}  :  {self.transactionid} : {self.category }"
