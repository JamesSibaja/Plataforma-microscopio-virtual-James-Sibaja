import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VirtualMicroscope.settings')
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from Projects import consumers

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    ]),
})