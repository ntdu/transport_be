from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, datetime as dt_class
from django.utils import timezone

from apiHelper.apiHelper import ApiHelper
from customer.models import Customer


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def listUser(request):
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


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getUser(request):
    try:
        phone_number = request.GET.get('phone')
        query = Customer.objects.filter(is_deleted=False, login_account__username=phone_number).values(
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


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateUser(request):
    try:
        form = ApiHelper.getData(request)

        login_account__username = form['login_account__username']
        first_name = form['first_name']
        last_name = form['last_name']
        female = form['female']
        date_of_birth = dt_class.strptime(
            form['date_of_birth'], '%Y-%m-%d')
        address = form['address']

        try:
            customer_update = Customer.objects.filter(
                is_deleted=False, login_account__username=login_account__username).first()
            customer_update.first_name = first_name
            customer_update.last_name = last_name
            customer_update.female = female
            customer_update.date_of_birth = date_of_birth
            customer_update.address = address
            customer_update.created_date = timezone.now()
            customer_update.save()
        except Exception as e:
            print(e)
            return ApiHelper.response_client_error("Sai kiểu dữ liệu")

        return ApiHelper.response_ok("Success")
    except Exception as e:
        print(e)
        return ApiHelper.response_error()


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def activateCustomer(request):
    try:
        form = ApiHelper.getData(request)
        login_account__username = form['login_account__username']

        customer = Customer.objects.filter(
            is_deleted=False, login_account__username=login_account__username).first()

        if not customer:
            return ApiHelper.Response_info("Không tìm thấy tài khoản")

        customer.is_active = True
        customer.save()

        return ApiHelper.Response_ok("Success")
    except Exception as e:
        print(e)
        return ApiHelper.Response_error()


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deactivateCustomer(request):
    try:
        form = ApiHelper.getData(request)
        login_account__username = form['login_account__username']

        customer = Customer.objects.filter(
            is_deleted=False, login_account__username=login_account__username).first()

        if not customer:
            return ApiHelper.response_info("Không tìm thấy tài khoản")

        customer.is_active = not(customer.is_active)
        customer.save()

        return ApiHelper.response_ok("Success")
    except Exception as e:
        print(e)
        return ApiHelper.response_error()
