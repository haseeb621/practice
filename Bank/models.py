from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    inst_num = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banks')

class Branch(models.Model):
    name = models.CharField(max_length=100)
    transit_num = models.CharField(max_length=100)
    address = models.TextField()  
    email = models.EmailField()  
    capacity = models.CharField(max_length=100)
    Bank_id=models.ForeignKey(Bank,on_delete=models.CASCADE, related_name='branches')
