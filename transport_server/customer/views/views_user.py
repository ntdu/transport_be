from django.contrib.auth.decorators import login_required, permission_required 
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.http import JsonResponse, HttpResponse
from datetime import datetime as dt_class
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from apiHelper.apiHelper import ApiHelper
from customer.models import Customer

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def register(request):  
    try:
        form = ApiHelper.getData(request)
        email = form['email']
        password = form['password']
        firstName = form['firstName']
        lastName = form['lastName']
        phoneNumber = form['phoneNumber']
        gender = form['gender']
        dateOfBirth = dt_class.strptime(form['dateOfBirth'], '%Y-%m-%d')
        address = form['address']

        try:
            user = User.objects.create_user(username=phoneNumber, email=email, password=password)
            user.save()
        except:
            return ApiHelper.response_client_error('phoneNumber was exist')
    
        customer = Customer(
            login_account=user,
            email=email,
            first_name=firstName,
            last_name=lastName,
            female=gender,
            date_of_birth = dateOfBirth,
            address=address
        )
        customer.save()

        token,_ = Token.objects.get_or_create(user=user)
        return ApiHelper.response_ok({
            'token': token.key,
        })

    except Exception as e:
        print(e)
        return ApiHelper.response_error(e)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def login(request):  
    try:
        form = ApiHelper.getData(request)
        username = form['username']
        password = form['password']

        user = authenticate(request, username=username, password=password)
        if not user:
            return ApiHelper.response_error('Tên đăng nhập hoặc mật khẩu không đúng')

        token,_ = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'token': token.key
        }) 
        # return ApiHelper.response_ok({
        #     'token': token.key
        # })

    except Exception as e:
        print(e)
        return ApiHelper.response_error(e)