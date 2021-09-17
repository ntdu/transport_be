from django.contrib.auth.decorators import login_required, permission_required 
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.http import JsonResponse, HttpResponse
from datetime import datetime as dt_class
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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

        user = User.objects.create_user(username=phoneNumber, email=email, password=password)
        user.save()

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

        # form =  ApiHelper.getData(request)
        
        # password = form['password']
        
        # user = User.objects.filter(username=request.user.username).first()
        # user.set_password(password)   
        # user.save()

        # return ApiHelper.Response_ok('ok')
    except Exception as e:
        print(e)
        return ApiHelper.response_error()