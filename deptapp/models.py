from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin,AbstractBaseUser

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
    status = models.BooleanField(default=True)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    role = models.ForeignKey('Roles', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('Depart', on_delete=models.SET_NULL, null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField(auto_now_add=True)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# class Users(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     mobile = models.CharField(max_length=10)
#     role = models.ForeignKey('Roles', on_delete=models.SET_NULL, null=True)
#     department = models.ForeignKey('Depart', on_delete=models.SET_NULL, null=True)
#     reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
#     date_of_joining = models.DateField()
#     username=models.CharField(unique=True,max_length=100)
#     password=models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 