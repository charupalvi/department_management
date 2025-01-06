'''
application - deptpp urls.py file
'''

from django.urls import path
from deptapp import views

urlpatterns = [
    # Departments:
    path('',views.showHome),
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
]
