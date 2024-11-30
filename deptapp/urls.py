'''
application - deptpp urls.py file
'''

from django.urls import path
from deptapp import views

urlpatterns = [
    path('',views.showHome),
    path('modifydepart',views.modifyDepart),
    path('adddepart',views.addDepart),
    path('delete/<int:departid>',views.Deletedepart),
    path('update/<int:departid>',views.Updatedepart),


]
