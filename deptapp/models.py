from django.db import models

# Create your models here.
class Depart(models.Model):
    dept_id = models.AutoField(primary_key=True)
    depart_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=True)