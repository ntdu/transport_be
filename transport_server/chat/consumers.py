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

            driver = DriverOnline.objects.filter(customer__login_account__username=driver_phone).first().customer
            # shipment = Shipment(
            #     driver = driver,
            #     customer_ready = customer_ready,
            #     price = price
            # )
            # shipment.save()

            destination_info = DestinationInfo.objects.filter(customer_ready=customer_ready).first()
            message = {
                'type': 'DELIVERY_BIKER_CHOSEN_EVENT',
                'data': {
                    'coordinates': {
                        'origin': {
                            'lng': float(customer_ready.origin_lng),
                            'lat': float(customer_ready.origin_lat)
                        },
                        'destination': {
                            'lng': float(destination_info.destination_lng),
                            'lat': float(destination_info.destination_lat)
                        }
                    },
                    'address': {
                        'origin': customer_ready.origin_address,
                        'destination': destination_info.destination_address
                    },
                    'sender': {
                        'phone_number': customer.login_account.username,
                        'email': customer.email,
                        'first_name': customer.first_name,
                        'last_name': customer.last_name,
                        'female': customer.female,
                        'date_of_birth': customer.display_date_of_birth(),
                        'created_date': customer.display_created_date()
                    },
                    'receiver': {
                        'phone': destination_info.phone,
                        'name': destination_info.name
                    },
                    'price': price,
                    'deliveryHash': 'adfafdb',
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
            
            data = text_data_json['message']['data']
            origin_lng = data['coordinates']['origin']['lng']
            origin_lat = data['coordinates']['origin']['lat']
            origin_address = data['address']['origin']
            
            phone = data['receiver']['phone']
            name = data['receiver']['name']
            destination_lng = data['coordinates']['destination']['lng']
            destination_lat = data['coordinates']['destination']['lat']
            destination_address = data['address']['destination']
            weight = data['package']['weight']

            customer_ready = CustomerReady(
                customer = customer,
                origin_lng = origin_lng,
                origin_lat = origin_lat,
                origin_address = origin_address
            )
            customer_ready.save()

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

            driver_online = DriverOnline.objects.all().first()

            phone = driver_online.customer.login_account.username
            loc_customer = (origin_lng, origin_lat)
            loc_driver = (driver_online.longitude, driver_online.latitude)
            distance = hs.haversine(loc_customer,loc_driver)

            message = {
                'type': 'DELIVERY_BOOKING',
                'data': [
                    {
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
                    }
                ]
            }  

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

            # 'phone':
            # 'distance':
            # 'userDetail': {
            #     'accountUsername'
            #     'address'
            #     'dateOfBirth'
            #     'firstName'
            #     'gender'
            #     'lastName'
            #     'phoneNumber'
            # }
        
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

            destination_info = DestinationInfo.objects.filter(customer_ready=customer_ready).first()
            message = {
                'type': 'DELIVERY_BIKER_CHOSEN_EVENT',
                'data': {
                    'coordinates': {
                        'origin': {
                            'lng': float(customer_ready.origin_lng),
                            'lat': float(customer_ready.origin_lat)
                        },
                        'destination': {
                            'lng': float(destination_info.destination_lng),
                            'lat': float(destination_info.destination_lat)
                        }
                    },
                    'address': {
                        'origin': customer_ready.origin_address,
                        'destination': destination_info.destination_address
                    },
                    'sender': {
                        'phone_number': customer.login_account.username,
                        'email': customer.email,
                        'first_name': customer.first_name,
                        'last_name': customer.last_name,
                        'female': customer.female,
                        'date_of_birth': customer.display_date_of_birth(),
                        'created_date': customer.display_created_date()
                    },
                    'receiver': {
                        'phone': destination_info.phone,
                        'name': destination_info.name
                    },
                    'price': price,
                    'deliveryHash': 'adfafdb',
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

        """ DRIVER """
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