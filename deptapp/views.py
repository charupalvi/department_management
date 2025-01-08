from django.shortcuts import render, redirect, get_object_or_404
from deptapp.models import Depart, Roles, Users,Task
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from random import randint
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse



# Utility function to check if the user is admin
def is_admin(user):
    try:
        print(f"User role: {user.role.role_name}")  # Debugging log
        # print(request.session.items())  # This will print the session data
        return user.role.role_name == 'Admin'  # Ensure 'role_name' is correctly matching
    except AttributeError:
        # print(request.session.items())  # This will print the session data
        return False


# Show home page
def showHome(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    context = {
        'is_authenticated': bool(user),
        'user': user,
        'role': user.role.role_name if user and user.role else 'No Role Assigned',
    }
    return render(request, 'index.html', context)

# View departments (only active)
def viewDepart(request):
    data = Depart.objects.filter(status=True)
    context = {'departs': data}
    return render(request, 'viewdepart.html', context)

# Modify departments (only for admins)
def modifyDepart(request):    
    data = Depart.objects.filter(status=True)
    context = {'departs': data}
    return render(request, 'modifydepart.html', context)

# Add a department (only for admins)
def addDepart(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    if request.method == 'GET':
        return render(request, 'adddepart.html')
    else:
        n = request.POST['depart_name']
        d = request.POST['description']
        Depart.objects.create(depart_name=n, description=d)
        return redirect('/modifydepart')

# Delete department (only for admins)
def Deletedepart(request, departid):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    depart = Depart.objects.get(dept_id=departid)
    depart.status = False
    depart.save()
    return redirect('/modifydepart')

# Update department (only for admins)
def Updatedepart(request, departid):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    d = Depart.objects.get(dept_id=departid)
    if request.method == 'GET':
        context = {'depart': d}
        return render(request, 'updatedepart.html', context)
    else:
        n = request.POST['depart_name']
        d.description = request.POST['description']
        d.depart_name = n
        d.save()
        return redirect('/modifydepart')

# View roles (only active)
def viewRole(request):
    data = Roles.objects.filter(status=True)
    context = {'roles': data}
    return render(request, 'viewrole.html', context)

# Add a role (only for admins)
def addRole(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    if request.method == 'GET':
        return render(request, 'addrole.html')
    else:
        n = request.POST['role_name']
        d = request.POST['description']
        Roles.objects.create(role_name=n, description=d)
        return redirect('/viewrole')

# Delete role (only for admins)
def Deleterole(request, roleid):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    role = Roles.objects.get(role_id=roleid)
    role.status = False
    role.save()
    return redirect('/viewrole')

# Update role (only for admins)
def Updaterole(request, roleid):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    r = Roles.objects.get(role_id=roleid)
    if request.method == 'GET':
        context = {'role': r}
        return render(request, 'updaterole.html', context)
    else:
        n = request.POST['role_name']
        r.description = request.POST['description']
        r.role_name = n
        r.save()
        return redirect('/viewrole')

# View employees
def view_employees(request):
    employees = Users.objects.all()
    return render(request, 'view_employees.html', {'employees': employees})

# Add an employee (only for admins)
def add_employee(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    if request.method == 'GET':
        roles = Roles.objects.all()
        departments = Depart.objects.filter(status=True)
        return render(request, 'addemployee.html', {
            'roles': roles,
            'departments': departments
        })
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        role_id = request.POST.get('role')
        department_id = request.POST.get('department')
        date_of_joining = request.POST['date_of_joining']
        username = request.POST['username']
        password = request.POST['password']

        role = Roles.objects.get(role_id=role_id)
        department = Depart.objects.get(dept_id=department_id)

        try:
            Users.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                role=role,
                department=department,
                date_of_joining=date_of_joining,
                username=username,
                password=make_password(password)
            )
            return redirect('/viewemployees')
        except IntegrityError:
            messages.error(request, f"Username '{username}' is already taken. Please choose another one.")
            return render(request, 'addemployee.html', {
                'roles': Roles.objects.all(),
                'departments': Depart.objects.filter(status=True),
                'username_error': True
            })

# Update employee (only for admins)
def update_employee(request, employee_id):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    employee = get_object_or_404(Users, id=employee_id)
    if request.method == 'POST':
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.email = request.POST['email']
        employee.mobile = request.POST['mobile']
        employee.role = Roles.objects.get(role_id=request.POST['role'])
        employee.department = Depart.objects.get(dept_id=request.POST['department'])
        employee.date_of_joining = request.POST['date_of_joining']
        employee.save()
        return redirect('/viewemployees')
    else:
        roles = Roles.objects.all()
        departments = Depart.objects.filter(status=True)
        return render(request, 'update_delete_employee.html', {
            'employee': employee,
            'roles': roles,
            'departments': departments
        })

# Delete employee (only for admins)
def delete_employee(request, employee_id):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    employee = get_object_or_404(Users, id=employee_id)
    employee.delete()
    return redirect('/viewemployees')


# User Login:

# Dictionary to temporarily store OTPs
otp_storage = {}

def login_view(request):
    next_url = request.GET.get('next', '/')  # Retrieve next URL parameter if available
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect(next_url)  # Redirect to original page
            else:
                messages.error(request, 'Invalid password.')
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'login.html')



# Logout view
def logout_view(request):
    logout(request)
    return redirect('/login/')


# Password reset request
def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = Users.objects.get(email=email)
            otp = randint(100000, 999999)
            otp_storage[email] = otp

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP is {otp}',
                'dcharlie919@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your registered email.')
            return redirect('/validateotp/')
        except Users.DoesNotExist:
            messages.error(request, 'Email not registered.')
    return render(request, 'reset_password_request.html')

# OTP validation
def validate_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        entered_otp = request.POST['otp']
        if otp_storage.get(email) == int(entered_otp):
            return redirect(f'/resetpassword/?email={email}')
        else:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'validate_otp.html')

# Reset password
def reset_password(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        new_password = request.POST['password']
        user = Users.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        messages.success(request, 'Password reset successful. Please login.')
        return redirect('/login/')
    return render(request, 'reset_password.html', {'email': email})


# Tasks
# View tasks

# def view_tasks(request):
#     # Get the status filter from the URL
#     status_filter = request.GET.get('status', None)

#     # Get the employee filter from the URL
#     employee_filter = request.GET.get('employee_filter', None)

#     # Get the start and end date filters from the URL
#     start_date = request.GET.get('start_date', None)
#     end_date = request.GET.get('end_date', None)

#     # Filter tasks based on provided filters
#     tasks = Task.objects.all()

#     # Filter by status
#     if status_filter:
#         tasks = tasks.filter(status=status_filter)

#     # Filter by employee (assigned_to)
#     if employee_filter and employee_filter != 'all':
#         tasks = tasks.filter(assigned_to_id=employee_filter)

#     # Filter by date range (start_date and end_date)
#     if start_date and end_date:
#         tasks = tasks.filter(start_date__gte=start_date, end_date__lte=end_date)
#     elif start_date:
#         tasks = tasks.filter(start_date__gte=start_date)
#     elif end_date:
#         tasks = tasks.filter(end_date__lte=end_date)

#     # Pagination: Show 10 tasks per page
#     page = request.GET.get('page', 1)
#     paginator = Paginator(tasks, 10)
#     tasks = paginator.get_page(page)

#     # Get the count of tasks by status
#     completed_count = Task.objects.filter(status='Completed').count()
#     in_progress_count = Task.objects.filter(status='In Progress').count()
#     pending_count = Task.objects.filter(status='Pending').count()
#     total_count = tasks.paginator.count

#     # Get employees for the employee filter dropdown
#     employees = Users.objects.all()

#     # Context to pass to the template
#     context = {
#         'tasks': tasks,
#         'status_filter': status_filter,
#         'employee_filter': employee_filter,
#         'start_date': start_date,
#         'end_date': end_date,
#         'employees': employees,
#         'completed_count': completed_count,
#         'in_progress_count': in_progress_count,
#         'pending_count': pending_count,
#         'total_count': total_count,
#     }

#     return render(request, 'view_tasks.html', context)

# def view_tasks(request):
#     # Fetch query parameters from GET request
#     status_filter = request.GET.get('status', None)
#     employee_filter = request.GET.get('employee_filter', None)
#     start_date = request.GET.get('start_date', None)
#     end_date = request.GET.get('end_date', None)

#     tasks = Task.objects.all()

#     # Apply filters based on status
#     if status_filter:
#         tasks = tasks.filter(status=status_filter)

#     # Apply filter for employee if selected
#     if employee_filter and employee_filter != 'all':
#         tasks = tasks.filter(assigned_to__id=employee_filter)

#     # Apply date range filter
#     if start_date:
#         tasks = tasks.filter(start_date__gte=start_date)
#     if end_date:
#         tasks = tasks.filter(end_date__lte=end_date)

#     # Fetch statistics for the graph
#     completed_count = tasks.filter(status='completed').count()
#     in_progress_count = tasks.filter(status='in_progress').count()
#     pending_count = tasks.filter(status='pending').count()

#     # Paginate tasks
#     from django.core.paginator import Paginator
#     paginator = Paginator(tasks, 10)  # Show 10 tasks per page
#     page_number = request.GET.get('page')
#     tasks_page = paginator.get_page(page_number)

#     # Fetch employees for the filter dropdown
#     employees = Users.objects.all()

#     return render(request, 'view_tasks.html', {
#         'tasks': tasks_page,
#         'completed_count': completed_count,
#         'in_progress_count': in_progress_count,
#         'pending_count': pending_count,
#         'employees': employees,
#     })
    

def view_tasks(request):
    tasks = Task.objects.filter(assigned_to__reporting_manager=request.user)

    # Filter by employee
    employee_id = request.GET.get('employee_filter')
    if employee_id and employee_id != "all":
        tasks = tasks.filter(assigned_to_id=employee_id)

    # Filter by status
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        tasks = tasks.filter(start_date__gte=start_date, end_date__lte=end_date)

    # Task statistics (counts)
    completed_count = tasks.filter(status='Completed').count()
    in_progress_count = tasks.filter(status='In Progress').count()
    pending_count = tasks.filter(status='Pending').count()

    # Paginate tasks
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    tasks_page = paginator.get_page(page_number)

    # Fetch employees for the filter dropdown
    # employees = Users.objects.all()
    # employees = Users.objects.filter(tasks__isnull=False).distinct()
    employees = Users.objects.filter(tasks__isnull=False).values('id', 'first_name', 'last_name').distinct()


    # Pass tasks and task statistics to the template
    context = {
        'tasks': tasks,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'pending_count': pending_count,
        'employees': employees,
        'tasks_page':tasks_page
    }

    return render(request, 'view_tasks.html', context)
    
# Add a task
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        priority = request.POST['priority']
        task_type = request.POST['task_type']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        assigned_to = Users.objects.get(id=request.POST['assigned_to'])
        Task.objects.create(
            title=title, description=description, priority=priority,
            task_type=task_type, start_date=start_date, end_date=end_date,
            assigned_to=assigned_to, created_by=request.user
        )
        return redirect('viewtasks')
    employees = Users.objects.filter(reporting_manager=request.user)
    return render(request, 'add_task.html', {'employees': employees})

# Edit a task
def edit_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.priority = request.POST['priority']
        task.task_type = request.POST['task_type']
        task.start_date = request.POST['start_date']
        task.end_date = request.POST['end_date']
        task.status = request.POST['status']
        task.save()
        return redirect('viewtasks')
    employees = Users.objects.filter(reporting_manager=request.user)
    return render(request, 'edit_task.html', {'task': task, 'employees': employees})

# Delete a task
def delete_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    task.delete()
    return redirect('viewtasks')

def mark_completed(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)  # Use task_id here
    task.status = 'Completed'
    task.save()
    return redirect('viewtasks')

def task_details(request, task_id):
    # Use task_id for fetching task details
    task = get_object_or_404(Task, task_id=task_id)

    context = {
        'task': task
    }
    
    return render(request, 'task_details.html', context)


