'''
application - deptpp urls.py file
'''

from django.urls import path
from deptapp import views

urlpatterns = [
    # Departments:
    path('',views.showHome),
    path('viewdepart',views.viewDepart),
    path('modifydepart',views.modifyDepart),
    path('adddepart',views.addDepart),
    path('delete/<int:departid>',views.Deletedepart),
    path('update/<int:departid>',views.Updatedepart),
    #Roles:
    path('viewrole',views.viewRole),
    path('addrole',views.addRole),
    path('deleterole/<int:roleid>',views.Deleterole),
    path('updaterole/<int:roleid>',views.Updaterole),
    # Employees:
    path('viewemployees/', views.view_employees, name='viewemployees'),
    path('addemployee/', views.add_employee, name='addemployee'),
    path('updateemployee/<int:employee_id>/', views.update_employee, name='updateemployee'),
    path('deleteemployee/<int:employee_id>/', views.delete_employee, name='deleteemployee'),
    # User Login:
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('resetpasswordrequest/', views.reset_password_request, name='resetpasswordrequest'),
    path('validateotp/', views.validate_otp, name='validateotp'),
    path('resetpassword/', views.reset_password, name='resetpassword'),
    # Task :
    path('viewtasks/', views.view_tasks, name='viewtasks'),
    path('addtask/', views.add_task, name='addtask'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('mark_completed/<int:task_id>/', views.mark_completed, name='mark_completed'),
    path('task-details/<int:task_id>/', views.task_details, name='task_details'),

]
