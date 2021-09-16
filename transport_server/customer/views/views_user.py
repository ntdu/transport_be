from django.contrib.auth.decorators import login_required, permission_required 
from django.http import JsonResponse, HttpResponse

def register(request):  
    try:
        # form =  ApiHelper.getData(request)
        
        # password = form['password']
        
        # user = User.objects.filter(username=request.user.username).first()
        # user.set_password(password)   
        # user.save()

        return HttpResponse("ok")
    except Exception as e:
        print(e)
        return ApiHelper.Response_error()