from django.http import JsonResponse, HttpResponse 
import simplejson as json

class ApiHelper:
    @staticmethod
    def getData(request):
        return json.loads(request.body.decode('utf-8'))

    @staticmethod
    def Response_ok(data):
        return JsonResponse({
            'code': 200,
            'data': data
        })

    @staticmethod
    def Response_info(data):
        return JsonResponse({
            'code': 100,
            'data': data
        })

    @staticmethod
    def Response_client_error(data):
        return JsonResponse({
            'code': 400,
            'data': data
        }) 
    
    @staticmethod
    def Response_error():
        return HttpResponse(status=500)