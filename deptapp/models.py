from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Depart(models.Model):
    dept_id = models.AutoField(primary_key=True)
    depart_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=True)
    
class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    role = models.ForeignKey('Roles', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('Depart', on_delete=models.SET_NULL, null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField()
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=255)