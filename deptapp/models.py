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

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    task_type = models.CharField(max_length=20, choices=[('Individual', 'Individual'), ('Team', 'Team')])
    assigned_to = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='created_tasks')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Task_Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)  # Unique identification of task
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='assignments')  # Reference to Task table
    employee = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='assigned_tasks')  # Reference to Employee table (assigned to)
    assigned_by = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='tasks_assigned')  # Reference to Employee table (assigned by)
    assigned_date = models.DateTimeField(auto_now_add=True)  # Timestamp at which task is assigned
    status = models.CharField(
        max_length=200,
        choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
        default='Pending'
    )  # Status of the task
    completed_at = models.DateTimeField(null=True, blank=True)  # Timestamp at which task is completed

    def __str__(self):
        return f"Assignment {self.assignment_id} - Task {self.task.title}"
    
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)  # Unique identification of the review
    review_title = models.CharField(max_length=100)  # Title or small details of the review
    review_date = models.DateField()  # Date on which the review is taken
    employee = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='reviews')  # Reference to employee reviewed
    reviewed_by = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='reviews_given')  # Reference to reviewer
    review_period = models.CharField(max_length=100, choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annually', 'Annually')])  # Review period
    rating = models.IntegerField()  # Rating given to employee between 1-10
    comments = models.CharField(max_length=300, blank=True, null=True)  # Extra comments by reviewer
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when review was first created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when review was last updated

    def __str__(self):
        return f"Review {self.review_id} for {self.employee.username}"



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