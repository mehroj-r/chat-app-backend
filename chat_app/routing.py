from django.urls import path
from .consumers import Consumer

websocket_urlpatterns = [
    path('ws/chat/<chat_id>/', Consumer.as_asgi()),
]
