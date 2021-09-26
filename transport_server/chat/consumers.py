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
        self.send(text_data=json.dumps({
            'message': '\n...Đã kết nối'
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
        from chat.models import CustomerReady, DestinationInfo
        from customer.models import Customer

        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'CHAT':
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

            message = customer.first_name
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

            message = 'BIKER_WAITING_SUCCESS'
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