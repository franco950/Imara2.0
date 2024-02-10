from django.db import models
class staff_member(models.Model):
    staffid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    department=models.CharField(max_length=20) 
    location=models.CharField(max_length=20)

    def __str__(self):
        return f"{str(self.staffid)}  :  {self.name} : {self.department} : {self.location}"

