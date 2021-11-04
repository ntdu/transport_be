from django.urls import path

from . import views

app_name = 'biker'
urlpatterns = [
  path('list-user', views.listUser , name='listUser'),
  path('get-user', views.getUser , name='getUser'),
  path('update-user', views.updateUser , name='updateUser'),
  path('activate-customer', views.activateCustomer, name='activateCustomer'),
  path('deactivate-customer', views.deactivateCustomer, name='deactivateCustomer')
]