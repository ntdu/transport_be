from django.contrib.auth.decorators import login_required, permission_required 
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.http import JsonResponse, HttpResponse
from apiHelper.apiHelper import ApiHelper


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def register(request):  
    try:
        # form =  ApiHelper.getData(request)
        
        # password = form['password']
        
        # user = User.objects.filter(username=request.user.username).first()
        # user.set_password(password)   
        # user.save()

        return ApiHelper.Response_ok('ok')
    except Exception as e:
        print(e)
        return ApiHelper.Response_error()