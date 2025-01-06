from django.shortcuts import render,redirect,get_object_or_404
from deptapp.models import Depart,Roles,Users
from django.contrib.auth.hashers import make_password
# Create your views here.


# def showHome(request):
#     data=Depart.objects.all()
#     print(type(data)) # QuerySet of List containing
#     print(data)
#     context={}
#     context['departs']=data
#     return render(request,'index.html',context)

def showHome(request):
    # Only get active departments
    data = Depart.objects.filter(status=True)
    context = {'departs': data}
    return render(request, 'viewdepart.html', context)

def modifyDepart(request):
    # Only get active departments
    data = Depart.objects.filter(status=True)
    context = {'departs': data}
    return render(request, 'index.html', context)

def addDepart(request):
    print(request.method)
    if request.method=='GET':
        return render(request,'adddepart.html')
    else:
        #capture data from form
        n = request.POST['depart_name']
        d = request.POST['description']
        print(n,d)

        #add the data in db
        d=Depart.objects.create(depart_name=n,description=d)
        d.save()
        # return render(request,'index.html')
        # return render(request,'index.html',context)
        return redirect('/')
    
# def Deletedepart(request,departid):
#     depart=Depart.objects.filter(id=departid)
#     depart.delete()
#     return redirect('/')

def Deletedepart(request, departid):
    # Get the department object
    depart = Depart.objects.get(dept_id=departid)
    # Update the status to False (inactive)
    depart.status = False
    depart.save()  # Save the updated status to the database
    return redirect('/')

def Updatedepart(request,departid):
    # b=Depart.objects.filter(id=bookid)
    d=Depart.objects.get(dept_id=departid) 
    if request.method=='GET':
        context={}
        context['depart']=d # used with GET method
        return render(request,'updatedepart.html',context)
    else:
        dt=Depart.objects.filter(dept_id=departid)
        n=request.POST['depart_name']
        d=request.POST['description']
        dt.update(depart_name=n,description=d)
        return redirect('/')

# Roles :-

def viewRole(request):
    data=Roles.objects.all()
    print(type(data)) # QuerySet of List containing
    print(data)
    context={}
    context['roles']=data
    return render(request,'viewrole.html',context)


def addRole(request):
    print(request.method)
    if request.method=='GET':
        return render(request,'addrole.html')
    else:
        #capture data from form
        n = request.POST['role_name']
        d = request.POST['description']
        print(n,d)

        #add the data in db
        r=Roles.objects.create(role_name=n,description=d)
        r.save()
        # return render(request,'index.html')
        # return render(request,'index.html',context)
        return redirect('/viewrole')
    

def Deleterole(request, roleid):
    # Get the department object
    role = Roles.objects.get(role_id=roleid)
    # Update the status to False (inactive)
    role.status = False
    role.save()  # Save the updated status to the database
    return redirect('/viewrole')

def Updaterole(request,roleid):
    # b=Depart.objects.filter(id=bookid)
    r=Roles.objects.get(role_id=roleid) 
    if request.method=='GET':
        context={}
        context['role']=r # used with GET method
        return render(request,'updaterole.html',context)
    else:
        ur=Roles.objects.filter(role_id=roleid)
        n=request.POST['role_name']
        d=request.POST['description']
        ur.update(role_name=n,description=d)
        return redirect('/viewrole')
    
#User / Employee :-

def view_employees(request):
    employees = Users.objects.all()
    return render(request, 'view_employees.html', {'employees': employees})

def add_employee(request):
    if request.method == 'GET':
        roles = Roles.objects.all()
        departments = Depart.objects.filter(status=True)
        users = Users.objects.all()
        return render(request, 'addemployee.html', {
            'roles': roles,
            'departments': departments,
            'users': users
        })
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        
        role_id = request.POST.get('role')
        department_id = request.POST.get('department')
        reporting_manager_id = request.POST.get('reporting_manager')  # This can be empty

        role = Roles.objects.get(role_id=role_id)
        department = Depart.objects.get(dept_id=department_id)
        
        # Handle empty reporting_manager by setting it to None if not provided
        reporting_manager = None
        if reporting_manager_id:
            reporting_manager = Users.objects.get(id=reporting_manager_id)

        date_of_joining = request.POST['date_of_joining']
        username = request.POST['username']
        password = make_password(request.POST['password'])

        Users.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            role=role,
            department=department,
            reporting_manager=reporting_manager,  # This can be None
            date_of_joining=date_of_joining,
            username=username,
            password=password
        )

        return redirect('/viewemployees')



def update_employee(request, employee_id):
    employee = get_object_or_404(Users, id=employee_id)
    if request.method == 'POST':
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.email = request.POST['email']
        employee.mobile = request.POST['mobile']
        employee.role = Roles.objects.get(role_id=request.POST['role'])
        employee.department = Depart.objects.get(dept_id=request.POST['department'])
        employee.reporting_manager = Users.objects.get(id=request.POST['reporting_manager'])
        employee.date_of_joining = request.POST['date_of_joining']
        employee.save()
        return redirect('/viewemployees')
    else:
        roles = Roles.objects.all()
        departments = Depart.objects.filter(status=True)
        users = Users.objects.all()
        return render(request, 'update_delete_employee.html', {
            'employee': employee,
            'roles': roles,
            'departments': departments,
            'users': users
        })

def delete_employee(request, employee_id):
    employee = get_object_or_404(Users, id=employee_id)
    employee.delete()
    return redirect('/viewemployees')