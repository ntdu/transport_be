from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat import consumers as chat_consumers

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_server.settings')

application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', chat_consumers.ChatConsumer.as_asgi()),
            # re_path(r'ws/greenws/(?P<room_name>\w+)/$', greenws_consumers.GreenWSConsumer.as_asgi()),
        ])
    ),
})