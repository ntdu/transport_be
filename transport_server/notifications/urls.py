from django.urls import path

from . import views

app_name = 'notifications'
urlpatterns = [
    path('firebase-messaging-sw.js', views.show_firebase_js, name='show_firebase_js'),
    path('index', views.index),
    path('send-noti', views.sendNoti , name='sendNoti'),

]