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
    #Review Employee:
    path('reviews/', views.view_reviews, name='view_reviews'),
    path('addreview/', views.add_review, name='add_review'),
    path('see-comments/<int:review_id>/', views.see_comments, name='see_comments'),
    path('edit-review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    # Leave Management:
    path('leave_dashboard/', views.leave_dashboard, name='leave_dashboard'),
    path('leave_dashboard_employee/', views.leave_dashboard_employee, name='leave_dashboard_employee'),
    path('leave_dashboard_admin/', views.leave_dashboard_admin, name='leave_dashboard_admin'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('approve_or_reject_leave/<int:leave_id>/', views.approve_or_reject_leave, name='approve_or_reject_leave'),
    path('edit_leave/<int:leave_id>/', views.edit_leave, name='edit_leave'),
    path('leave-quota/', views.leave_quota_view, name='leave_quota_view'),
    path('leave-quota/edit/<int:employee_id>/', views.edit_leave_quota_view, name='edit_leave_quota'),


]
