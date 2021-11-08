from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, datetime as dt_class
from django.db.models import Count
from django.utils import timezone
from django.db.models import Sum, Q

from apiHelper.apiHelper import ApiHelper
from customer.models import Customer
from chat.models import Shipment, StatusShipment

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


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def shipmentReportTenDays(request):
    try:
        to_date = dt_class.now()
        from_date = to_date - timedelta(days=9)

        list_shipment_ten_days = list(Shipment.objects.filter(
            # is_deleted = False, 
            created_date__date__gte = from_date,
            created_date__date__lte = to_date,
        ).values('status', 'created_date__date').annotate(total=Count('id')))

        list_data = []
        list_date = []

        list_wait_confirm = []
        list_wait_pickup = []
        list_process = []
        list_success = []
        list_cancelled = []

        for date in  daterange(from_date, to_date):
            wait_confirm = 0
            wait_pickup = 0
            process = 0
            success = 0
            cancelled = 0

            list_date.append(date)
            for shipment_date in list_shipment_ten_days:
                if shipment_date['status'] == StatusShipment.WAIT_CONFIRM.value and shipment_date['created_date__date'] == date.date():
                    wait_confirm = shipment_date['total']
                if shipment_date['status'] == StatusShipment.WAIT_PICKUP.value and shipment_date['created_date__date'] == date.date():
                    wait_pickup = shipment_date['total']
                if shipment_date['status'] == StatusShipment.PROCESS.value and shipment_date['created_date__date'] == date.date():
                    process = shipment_date['total']
                if shipment_date['status'] == StatusShipment.SUCCESSED.value and shipment_date['created_date__date'] == date.date():
                    success = shipment_date['total']
                if shipment_date['status'] == StatusShipment.CANCELLED.value and shipment_date['created_date__date'] == date.date():
                    cancelled = shipment_date['total']
              
            list_wait_confirm.append(wait_confirm)
            list_wait_pickup.append(wait_pickup)
            list_process.append(process)
            list_success.append(success)
            list_cancelled.append(cancelled)                

        list_data.append({
            'status': StatusShipment.display(StatusShipment.WAIT_CONFIRM.value),
            'data': list_wait_confirm
        })
        list_data.append({
            'status': StatusShipment.display(StatusShipment.WAIT_PICKUP.value),
            'data': list_wait_pickup
        })
        list_data.append({
            'status': StatusShipment.display(StatusShipment.PROCESS.value),
            'data': list_process
        })
        list_data.append({
            'status': StatusShipment.display(StatusShipment.SUCCESSED.value),
            'data': list_success
        })
        list_data.append({
            'status': StatusShipment.display(StatusShipment.CANCELLED.value),
            'data': list_cancelled
        })

        return ApiHelper.response_ok({
            'list_date': list_date,
            'list_data': list_data
        }) 
    except Exception as ex:
        print(ex)
        return ApiHelper.response_err(500)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def newAccountBySixMonth(request):
    try:
        to_month = dt_class.now()
        from_month = monthdelta(to_month, -5)
        list_result = []

        for month in monthrange(from_month, to_month):
            list_new_id_account = []
            shipment_in_month = Shipment.objects.filter(
                # is_deleted = False, 
                status = StatusShipment.SUCCESSED.value,
                created_date__month = month.month,
                created_date__year = month.year
            )
            
            for shipment in shipment_in_month:
                new_shipment = Shipment.objects.filter(
                    # is_deleted = False, 
                    customer_ready__customer__id = shipment.customer_ready.customer.id, 
                    created_date__month__lt = month.month, 
                    created_date__year__lte = month.year
                )

                if new_shipment.count() == 0 and shipment.customer_ready.customer.id not in list_new_id_account:
                    list_new_id_account.append(shipment.customer_ready.customer.id)
            
            list_result.append({
                'month': month.strftime('%m/%Y'),
                'num_new_account': len(list_new_id_account),
                'list_new_id_account': list_new_id_account
            })

        return ApiHelper.response_ok(list_result)
    except Exception as ex:
        print(ex)
        return ApiHelper.response_error()


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getTopAccount(request):
    try:
        all_account = Customer.objects.filter(is_deleted=False)
        list_account_shipment = []

        for account in all_account:
            delivered_amount = Shipment.objects.filter(customer_ready__customer=account).count()
            query_shipment = Shipment.objects.filter(customer_ready__customer=account).aggregate(
                total_money = Sum('price')
            )
            print(query_shipment)
            # for sale_order in list(query_shipment):
            #     sale_order_detail = list(sale_order.salesorderdetail_set.filter(
            #         is_deleted=False
            #     ).values('sales_order').annotate(
            #         delivered_amount = Sum('delivered_amount'), 
            #         total_money = Sum('total_money')
            #     ))
                
            #     if sale_order_detail:
            #         delivered_amount += sale_order_detail[0]['delivered_amount']
            #         total_money += sale_order_detail[0]['total_money']

            list_account_shipment.append({
                'account': account.first_name,
                'delivered_amount': delivered_amount,
                'total_money': query_shipment['total_money'] if query_shipment['total_money'] else 600000
            })
            list_account_shipment = sorted(list_account_shipment, key = lambda i: i['delivered_amount'], reverse=True)

        return ApiHelper.response_ok(list_account_shipment)
    except Exception as ex:
        print(ex)
        return ApiHelper.response_error()


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(days=n)


def monthrange(start_date, end_date):
    start_date = start_date.replace(day=1)
    end_date = end_date.replace(day=1)
    date = start_date
    r = [ ]
    while date <= end_date:
        r.append(date) 
        date = (date + timedelta(days=31)).replace(day=1)
    return r


def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    return date.replace(day=1,month=m, year=y)

