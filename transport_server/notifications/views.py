from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, datetime as dt_class
from django.db.models import Count
from django.utils import timezone
from django.db.models import Sum, Q

from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

from apiHelper.apiHelper import ApiHelper
from customer.models import Customer
from chat.models import Shipment, StatusShipment, DestinationInfo

@api_view(['GET'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def sss(request):
    try:
        query = Customer.objects.filter(is_deleted=False).order_by("-created_date").values(
            'login_account__username',
            'email',
            'first_name',
            'last_name',
            'female',
            'date_of_birth',
            'address',
            'is_active',
            'created_date'
        )
        return ApiHelper.response_ok(list(query))
    except Exception as e:
        print(e)
        return ApiHelper.response_error()


def index(request):
    return render(request, 'index.html')

def show_firebase_js(request):
    data = '''
    importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
    importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

    firebase.initializeApp({
            apiKey: "AIzaSyC-6bZPkSILcGberTGlqOAX7tiow8K6Mxw",
              authDomain: "sopdev-86855.firebaseapp.com",
              databaseURL: "https://sopdev-86855-default-rtdb.asia-southeast1.firebasedatabase.app",
              projectId: "sopdev-86855",
              storageBucket: "sopdev-86855.appspot.com",
              messagingSenderId: "280112674639",
              appId: "1:280112674639:web:bfce500fbf7a60f28db73a",
              measurementId: "G-DKZSNDP153"
    });
    const messaging = firebase.messaging();

    messaging.onBackgroundMessage((payload) => {
        console.log("dasfsdfdf", payload);
        console.log(
            '[firebase-messaging-sw.js] Received background message ',
            payload
        );
        // Customize notification here
        const notificationTitle = 'Background Message Title';
        const notificationOptions = {
            body: 'Background Message body.',
            icon: '/firebase-logo.png'
        };

        self.registration.showNotification(notificationTitle, notificationOptions);
        });

    '''
    # messaging.setBackgroundMessageHandler((payload) => {
    # 
    return HttpResponse(data, content_type='text/javascript')


def send_notification(registration_ids, messages_title, message_desc):
    fcm_api = 'AAAAQTgEN08:APA91bFxkVMKj3sIcwX2NPYulkpsSwNfJohfklRzl55BK2JumqVWVnxJHDN7va52Ew46WmfKiHZfFYW4cUUqNfNl2CCQmfwn8c5cWFEVFDGeoyInlU84dpgzxR61z_unBl69inWrzwgV'
    url = 'https://fcm.googleapis.com/fcm/send'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + fcm_api
    }
    payload = {
        'registration_ids': registration_ids,
        'priority': 'high',
        'notification': {
            'body': 'mess',
            'title': 'title',
        }
    }
    
    result = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # print(result)
    print(result.json())
    
def sendNoti(request):
    registration = ['cquivquL9Ox3KQts_uH49F:APA91bEMRmYVDEAu7sBtXM3a2er-Pfx-5Sx71HuGXb6kYXtt8AA8xijmxC43MdNVhVkSYUHQb2PhhJXF3ryOxAbvn35ywswE0KRtk8QhXXRcRDEnCXUiXMNJIYQoqZzmItxXC2JajevD']
    send_notification(registration, 'Titile', 'Dess')
    
    return HttpResponse('sent')