from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.db.models import Q, Sum, Max, Min, Avg, Count
from datetime import datetime as dt_class, time, timedelta
from decimal import Decimal
# import bs4
# import pandas

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):

    socket_url = 'wss://' if request.is_secure() else 'ws://'
    socket_url += request.META['HTTP_HOST'] + '/ws/chat/' + room_name + '/'

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'socket_url': socket_url
    })