# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from rest_framework.authtoken.models import Token
# from chat.models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("connect")
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'message': '\n...Đã kết nối'
        # }))
        self.send(text_data=json.dumps({
            'message': {
                'type': 'ready',
                'data': '\n...Đã kết nối'
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        from rest_framework.authtoken.models import Token
        from chat.models import CustomerReady, DestinationInfo, DriverOnline, Shipment, StatusShipment
        from customer.models import Customer
        import haversine as hs

        
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'CHAT':
            customer = Customer.objects.filter(login_account__username='0354471333').first()
            customer_ready = CustomerReady.objects.filter(customer=customer).order_by('-created_date').first()

            # data = text_data_json['message']['data']
            driver_phone = '0354471332'
            price = '50000'

            # driver = DriverOnline.objects.filter(customer__login_account__username=driver_phone).first().customer
            # shipment = Shipment(
            #     driver = driver,
            #     customer_ready = customer_ready,
            #     price = price
            # )
            # shipment.save()

            list_destination_info = DestinationInfo.objects.filter(customer_ready=customer_ready)
            list_destination = []
            for destination_info in list_destination_info:
                list_destination.append({
                    'phoneNumber': destination_info.phone,
                    'name': destination_info.name,
                    'destinationLng': float(destination_info.destination_lng),
                    'destinationlLat': float(destination_info.destination_lat),
                    'address': destination_info.destination_address
                })
            message = {
                'type': 'DELIVERY_BIKER_CHOSEN_EVENT',
                'data': {
                    'originAndDestiationInfo': {
                        'origin': {
                            'sender': {
                                'accountUsername': customer.login_account.username,
                                'address': customer.address,
                                'dateOfBirth': customer.display_date_of_birth(),
                                'firstName': customer.first_name,
                                'gender': customer.female,
                                'lastName': customer.last_name,
                                'phoneNumber': customer.login_account.username,
                                'createdDate': customer.display_created_date()
                            },
                            'originalLng': float(customer_ready.origin_lng),
                            'originalLat': float(customer_ready.origin_lat),
                            'address': customer_ready.origin_address
                        },
                        'list_destination': list_destination,
                    },
                    'price': price,
                    'rideHash': 'N9TT-9G0A-B7FQ-RANC',
                    'package': {
                        'weight': float(destination_info.weight),
                    }
                }
            }

            # message = {
            #     'type': 'DELIVERY_BIKER_CHOSEN_EVENT',
            #     'data': 'price'
            # }
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

            # Send message to room group
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

        elif type == 'DELIVERY_BOOKING':
            token = text_data_json['message']['token']
            customer = Customer.objects.filter(login_account=Token.objects.get(key=token).user).first()
            
            packageInfor = text_data_json['message']['data']['packageInfor']

            origin_lng = packageInfor['originAndDestiationInfo']['origin']['originalLng']
            origin_lat = packageInfor['originAndDestiationInfo']['origin']['originalLat']
            origin_address = packageInfor['originAndDestiationInfo']['origin']['address']
            
            weight = packageInfor['weight']

            customer_ready = CustomerReady(
                customer = customer,
                origin_lng = origin_lng,
                origin_lat = origin_lat,
                origin_address = origin_address
            )
            customer_ready.save()

            list_destination = packageInfor['originAndDestiationInfo']['list_destination']
            distance = 0
            pre_location = (origin_lng, origin_lat)
            for item in list_destination:
                phone = item['phoneNumber']
                name = item['name']
                destination_lng = item['destinationLng']
                destination_lat = item['destinationLat']
                destination_address = item['address']

                des_location = (destination_lng, destination_lat)
                distance += hs.haversine(pre_location, des_location)

                destination_info = DestinationInfo(
                    customer_ready = customer_ready,
                    phone = phone,
                    name = name,
                    destination_lng = destination_lng,
                    destination_lat = destination_lat,
                    destination_address = destination_address,
                    weight = weight
                )
                destination_info.save()

            list_driver_online = DriverOnline.objects.all()

            list_data = []
            for driver_online in list_driver_online[:1]:
                phone = driver_online.customer.login_account.username

                list_data.append({
                    'phone': phone,
                    'distance': distance,
                    'userDetail': {
                        'email': driver_online.customer.email,
                        'address': driver_online.customer.address,
                        'date_of_birth': driver_online.customer.display_date_of_birth(),
                        'first_name': driver_online.customer.first_name,
                        'female': driver_online.customer.female,
                        'last_name': driver_online.customer.last_name,
                        'phone_number': phone,
                        'created_date': driver_online.customer.display_created_date(),
                    }
                })

            message = {
                'type': 'DELIVERY_BOOKING',
                'data': list_data
            }  

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        
        elif type == 'DELIVERY_BIKER_CHOSEN_EVENT':
            token = text_data_json['message']['token']
            customer = Customer.objects.filter(login_account=Token.objects.get(key=token).user).first()
            customer_ready = CustomerReady.objects.filter(customer=customer).order_by('-created_date').first()

            data = text_data_json['message']['data']
            driver_phone = data['biker']
            price = data['price']

            driver = DriverOnline.objects.filter(customer__login_account__username=driver_phone).first().customer
            shipment = Shipment(
                driver = driver,
                customer_ready = customer_ready,
                price = price
            )
            shipment.save()

            list_destination_info = DestinationInfo.objects.filter(customer_ready=customer_ready)
            list_destination = []
            for destination_info in list_destination_info:
                list_destination.append({
                    'phoneNumber': destination_info.phone,
                    'name': destination_info.name,
                    'destinationLng': float(destination_info.destination_lng),
                    'destinationlLat': float(destination_info.destination_lat),
                    'address': destination_info.destination_address
                })
            message = {
                'type': 'DELIVERY_BIKER_CHOSEN_EVENT',
                'data': {
                    # 'coordinates': {
                    #     'origin': {
                    #         'lng': float(customer_ready.origin_lng),
                    #         'lat': float(customer_ready.origin_lat)
                    #     },
                    #     'destination': {
                    #         'lng': float(destination_info.destination_lng),
                    #         'lat': float(destination_info.destination_lat)
                    #     }
                    # },
                    # 'address': {
                    #     'origin': customer_ready.origin_address,
                    #     'destination': destination_info.destination_address
                    # },
                    # 'sender': {
                    #     'phone_number': customer.login_account.username,
                    #     'email': customer.email,
                    #     'first_name': customer.first_name,
                    #     'last_name': customer.last_name,
                    #     'female': customer.female,
                    #     'date_of_birth': customer.display_date_of_birth(),
                    #     'created_date': customer.display_created_date()
                    # },
                    # 'receiver': {
                    #     'phone': destination_info.phone,
                    #     'name': destination_info.name
                    # },
                    # 'price': price,
                    # 'deliveryHash': 'adfafdb',
                    # 'package': {
                    #     'weight': float(destination_info.weight),
                    # }

                    'originAndDestiationInfo': {
                        'origin': {
                            'sender': {
                                'accountUsername': customer.login_account.username,
                                'address': customer.address,
                                'dateOfBirth': customer.display_date_of_birth(),
                                'firstName': customer.first_name,
                                'gender': customer.female,
                                'lastName': customer.last_name,
                                'phoneNumber': customer.login_account.username,
                                'createdDate': customer.display_created_date()
                            },
                            'originalLng': float(customer_ready.origin_lng),
                            'originalLat': float(customer_ready.origin_lat),
                            'address': customer_ready.origin_address
                        },
                        'list_destination': list_destination,
                    },
                    'price': price,
                    'rideHash': 'adfafdb',
                    'package': {
                        'weight': float(destination_info.weight),
                    }
                }
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

        elif type == 'BIKER_WAITING':
            token = text_data_json['message']['token']
            customer = Customer.objects.filter(login_account=Token.objects.get(key=token).user).first()

            data = text_data_json['message']['data']
            longitude = data['coordinates']['longitude']
            latitude = data['coordinates']['latitude']

            driver_online = DriverOnline.objects.filter(customer=customer).first()
            if driver_online:
                driver_online.longitude = longitude
                driver_online.longitude = longitude
                driver_online.save()
            else:
                driver_online = DriverOnline(
                    customer = customer,
                    longitude = longitude,
                    latitude = latitude
                )
                driver_online.save()

            message = {
                'type': 'BIKER_WAITING_SUCCESS',
                'data': 'Success'
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        
        elif type == 'DELIVERY_CONFIRMED_EVENT':
            token = text_data_json['message']['token']
            customer_phone = text_data_json['message']['data']['customer']

            driver = Customer.objects.filter(login_account=Token.objects.get(key=token).user).first()
            customer = Customer.objects.filter(login_account__username=customer_phone).first()

            # shipment = Shipment.objects.filter(driver=driver, customer_ready__customer=customer, status=StatusShipment.WAIT_CONFIRM.value).first()
            shipment = Shipment.objects.filter(driver=driver, customer_ready__customer=customer).first()
            shipment.status = StatusShipment.WAIT_PICKUP.value
            shipment.save()

            message = {
                'type': 'DELIVERY_CONFIRMED_EVENT',
                'data': shipment.id
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        
        elif type == 'DELIVERY_BIKER_WAITING':
            token = text_data_json['message']['token']
            print(token)
            driver = Customer.objects.filter(login_account=Token.objects.get(key=token).user).first()

            message = {
                'type': 'DELIVERY_BIKER_WAITING',
                'data': 'Tao đến r'
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        
        elif type == 'BIKER_RECEIVED_PACKAGE':
            token = text_data_json['message']['token']
            data = text_data_json['message']['data']

            deliveryHash = data['deliveryHash']
            bikerReceivedPackageProof = data['bikerReceivedPackageProof']

            print(deliveryHash)
            driver = Customer.objects.filter(login_account=Token.objects.get(key=token).user).first()

            message = {
                'type': 'BIKER_RECEIVED_PACKAGE',
                'data': 'Đã nhận hàng'
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        
        elif type == 'DELIVERY_COMPLETE_EVENT':
            token = text_data_json['message']['token']
            data = text_data_json['message']['data']

            deliveryHash = data['deliveryHash']
            deliverySuccessProof = data['deliverySuccessProof']

            print(deliveryHash)
            driver = Customer.objects.filter(login_account=Token.objects.get(key=token).user).first()

            message = {
                'type': 'DELIVERY_COMPLETE_EVENT',
                'data': 'Hoàn tất giao hàng'
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))