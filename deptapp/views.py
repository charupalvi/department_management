from django.shortcuts import render, redirect, get_object_or_404
from deptapp.models import Depart, Roles, Users,Task,Review
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
from django.db.models import Count




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
        users = Users.objects.filter(is_active=True)  # Get active users who can be selected as reporting managers
        return render(request, 'addemployee.html', {
            'roles': roles,
            'departments': departments,
            'users': users  # Pass the users to the template
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
        
        # Update the reporting manager if selected
        reporting_manager_id = request.POST.get('reporting_manager')
        if reporting_manager_id:
            employee.reporting_manager = Users.objects.get(id=reporting_manager_id)
        
        employee.save()
        return redirect('/viewemployees')
    else:
        roles = Roles.objects.all()
        departments = Depart.objects.filter(status=True)
        users = Users.objects.filter(is_active=True)  # Get active users who can be selected as reporting managers
        return render(request, 'update_delete_employee.html', {
            'employee': employee,
            'roles': roles,
            'departments': departments,
            'users': users  # Pass the users to the template
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
#     tasks = Task.objects.filter(assigned_to__reporting_manager=request.user)

#     # Filter by employee
#     employee_id = request.GET.get('employee_filter')
#     if employee_id and employee_id != "all":
#         tasks = tasks.filter(assigned_to_id=employee_id)
    
#     status = request.GET.get('status', '').strip()      
#     if status:
#         status_mapping = {              # Map the lowercase query params to the title-cased choices in the database
#             'pending': 'Pending',
#             'in_progress': 'In Progress',
#             'completed': 'Completed',
#             }
#         db_status = status_mapping.get(status.lower())
#         if db_status:
#             tasks = tasks.filter(status__iexact=db_status)  # Case-insensitive match
# # Filter by date range
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     if start_date and end_date:
#         # Parse date strings into datetime.date objects
#         start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#         end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

#         tasks = tasks.filter(
#             start_date__lte=end_date,
#             end_date__gte=start_date
#         )

#     print("Start Date:", start_date)
#     print("End Date:", end_date)
#     # Task statistics (counts)
#     completed_count = tasks.filter(status='Completed').count()
#     in_progress_count = tasks.filter(status='In Progress').count()
#     pending_count = tasks.filter(status='Pending').count()

#     # Paginate tasks
#     paginator = Paginator(tasks, 10)  # Show 10 tasks per page
#     page_number = request.GET.get('page')
#     tasks_page = paginator.get_page(page_number)

#     # Fetch employees for the filter dropdown
#     # employees = Users.objects.all()
#     # employees = Users.objects.filter(tasks__isnull=False).distinct()
#     employees = Users.objects.filter(tasks__isnull=False).values('id', 'first_name', 'last_name').distinct()


#     # Pass tasks and task statistics to the template
#     context = {
#         'tasks': tasks,
#         'completed_count': completed_count,
#         'in_progress_count': in_progress_count,
#         'pending_count': pending_count,
#         'employees': employees,
#         'tasks_page':tasks_page
#     }

#     return render(request, 'view_tasks.html', context)
    
    
def view_tasks(request):
    # Start with all tasks assigned to the reporting manager
    tasks = Task.objects.filter(assigned_to__reporting_manager=request.user)

    # Filter by employee (if selected)
    employee_id = request.GET.get('employee_filter')
    if employee_id and employee_id != "all":
        tasks = tasks.filter(assigned_to_id=employee_id)

    # Filter by status (if selected)
    status = request.GET.get('status', '').strip()      
    if status:
        status_mapping = {
            'pending': 'Pending',
            'in_progress': 'In Progress',
            'completed': 'Completed',
        }
        db_status = status_mapping.get(status.lower())
        if db_status:
            tasks = tasks.filter(status__iexact=db_status)

    # Filter by date range (if selected)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        # Parse the date strings into datetime.date objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        tasks = tasks.filter(
            start_date__lte=end_date,  # Task start date before or on the end date
            end_date__gte=start_date   # Task end date after or on the start date
        )

    # Task statistics (counts)
    completed_count = tasks.filter(status='Completed').count()
    in_progress_count = tasks.filter(status='In Progress').count()
    pending_count = tasks.filter(status='Pending').count()

    # Paginate tasks
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    tasks_page = paginator.get_page(page_number)

    # Fetch employees for the filter dropdown
    employees = Users.objects.filter(tasks__isnull=False).values('id', 'first_name', 'last_name').distinct()

    # Pass tasks and task statistics to the template
    context = {
        'tasks': tasks,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'pending_count': pending_count,
        'employees': employees,
        'tasks_page': tasks_page
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

# Review Employees

def view_reviews(request):
    # Extract query parameters for filtering
    department_filter = request.GET.get('department')
    employee_filter = request.GET.get('employee_filter')
    review_period = request.GET.get('review_period')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    rating_filter = request.GET.get('rating')
    search_employee = request.GET.get('search_employee')

    # Start with the base query
    reviews = Review.objects.all()

    # Apply filters
    if department_filter:
        reviews = reviews.filter(employee__department__id=department_filter)
    if employee_filter:
        reviews = reviews.filter(employee__id=employee_filter)
    if review_period:
        reviews = reviews.filter(review_period=review_period)
    if start_date and end_date:
        reviews = reviews.filter(review_date__range=[start_date, end_date])
    if rating_filter:
        if rating_filter == "1-5":
            reviews = reviews.filter(rating__range=(1, 5))
        elif rating_filter == "6-8":
            reviews = reviews.filter(rating__range=(6, 8))
        elif rating_filter == "9+":
            reviews = reviews.filter(rating__gte=9)
    if search_employee:
        reviews = reviews.filter(
            Q(employee__first_name__icontains=search_employee) |
            Q(employee__last_name__icontains=search_employee)
        )

    # Pagination
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    reviews_page = paginator.get_page(page_number)

    # Statistics for each period
    monthly_count = Review.objects.filter(review_period='Monthly').count()
    quarterly_count = Review.objects.filter(review_period='Quarterly').count()
    annual_count = Review.objects.filter(review_period='Annually').count()

    monthly_employees = Users.objects.filter(reviews__review_period='Monthly').distinct().count()
    quarterly_employees = Users.objects.filter(reviews__review_period='Quarterly').distinct().count()
    annual_employees = Users.objects.filter(reviews__review_period='Annually').distinct().count()

    # Calculate number of reviews per rating range for each period
    monthly_range_1_5 = Review.objects.filter(review_period='Monthly', rating__range=(1, 5)).count()
    monthly_range_6_8 = Review.objects.filter(review_period='Monthly', rating__range=(6, 8)).count()
    monthly_range_9_plus = Review.objects.filter(review_period='Monthly', rating__gte=9).count()

    quarterly_range_1_5 = Review.objects.filter(review_period='Quarterly', rating__range=(1, 5)).count()
    quarterly_range_6_8 = Review.objects.filter(review_period='Quarterly', rating__range=(6, 8)).count()
    quarterly_range_9_plus = Review.objects.filter(review_period='Quarterly', rating__gte=9).count()

    annual_range_1_5 = Review.objects.filter(review_period='Annually', rating__range=(1, 5)).count()
    annual_range_6_8 = Review.objects.filter(review_period='Annually', rating__range=(6, 8)).count()
    annual_range_9_plus = Review.objects.filter(review_period='Annually', rating__gte=9).count()

    # Number of employees per rating range
    range_1_5_employees = Review.objects.filter(rating__range=(1, 5)).values('employee').distinct().count()
    range_6_8_employees = Review.objects.filter(rating__range=(6, 8)).values('employee').distinct().count()
    range_9_plus_employees = Review.objects.filter(rating__gte=9).values('employee').distinct().count()

    # Pass data to the template
    context = {
        'reviews_page': reviews_page,
        'departments': Depart.objects.all(),
        'employees': Users.objects.all(),
        'monthly_count': monthly_count,
        'quarterly_count': quarterly_count,
        'annual_count': annual_count,
        'monthly_employees': monthly_employees,
        'quarterly_employees': quarterly_employees,
        'annual_employees': annual_employees,
        'monthly_range_1_5': monthly_range_1_5,
        'monthly_range_6_8': monthly_range_6_8,
        'monthly_range_9_plus': monthly_range_9_plus,
        'quarterly_range_1_5': quarterly_range_1_5,
        'quarterly_range_6_8': quarterly_range_6_8,
        'quarterly_range_9_plus': quarterly_range_9_plus,
        'annual_range_1_5': annual_range_1_5,
        'annual_range_6_8': annual_range_6_8,
        'annual_range_9_plus': annual_range_9_plus,
        'range_1_5_employees': range_1_5_employees,
        'range_6_8_employees': range_6_8_employees,
        'range_9_plus_employees': range_9_plus_employees,
    }
    return render(request, 'view_review.html', context)

def add_review(request):
    if request.method == 'POST':
        # Handle form submission and create a review
        employee_id = request.POST.get('employee_id')
        rating = request.POST.get('rating')
        review_period = request.POST.get('review_period')
        review_title = request.POST.get('review_title')
        comments = request.POST.get('comments')
        review_date = request.POST.get('review_date')

        # Ensure logged-in user is the reviewer
        reviewer = request.user

        # Create a new review object
        review = Review(
            employee_id=employee_id,
            rating=rating,
            review_period=review_period,
            review_title=review_title,
            comments=comments,
            review_date=review_date,
            reviewed_by=reviewer
        )
        review.save()

        return redirect('view_reviews')

    # Fetch employees to populate the dropdown
    employees = Users.objects.all()
    review_periods = Review._meta.get_field('review_period').choices  # Monthly, Quarterly, Annually

    context = {
        'employees': employees,
        'review_periods': review_periods,
    }

    return render(request, 'add_review.html', context)

def see_comments(request, review_id):
    # Fetch the review by its ID
    review = get_object_or_404(Review, review_id=review_id)

    # Pass the review (which already includes the comments field) to the context
    context = {
        'review': review
    }

    # Render the comments page with the review
    return render(request, 'see_comments.html', context)


def edit_review(request, review_id):
    # Fetch the review to edit
    review = get_object_or_404(Review, review_id=review_id)
    
    # Fetch employees and review periods for dropdown options
    employees = Users.objects.all()
    review_periods = Review._meta.get_field('review_period').choices
    
    # Create a list of ratings (1 to 10)
    ratings = list(range(1, 11))

    # If the form is submitted (POST request)
    if request.method == 'POST':
        # Get the data from the form
        employee_id = request.POST.get('employee_id')
        rating = request.POST.get('rating')
        review_period = request.POST.get('review_period')
        review_title = request.POST.get('review_title')
        comments = request.POST.get('comments')  # Get the updated comments
        review_date = request.POST.get('review_date')

        # Update the review with the new values
        review.employee_id = employee_id
        review.rating = rating
        review.review_period = review_period
        review.review_title = review_title
        review.comments = comments  # Update comments
        review.review_date = review_date

        # Save the updated review
        review.save()

        # Redirect to the review list with a success message
        messages.success(request, "Review updated successfully!")
        return redirect('view_reviews')

    # If the form is not submitted (GET request), render the edit form
    context = {
        'review': review,
        'employees': employees,
        'review_periods': review_periods,
        'ratings': ratings,  # Pass the ratings list to the template
    }
    return render(request, 'edit_review.html', context)

def delete_review(request, review_id):
    # Fetch the review to delete by its ID
    review = get_object_or_404(Review, review_id=review_id)
    
    # Delete the review
    review.delete()
    
    # Display a success message
    messages.success(request, "Review deleted successfully!")
    
    # Redirect back to the review list
    return redirect('view_reviews')