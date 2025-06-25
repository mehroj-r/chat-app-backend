from django.urls import path

from core.websocket.consumers.chat_list import ChatListConsumer
from core.websocket.consumers.messages import MessagesConsumer

ws_urlpatterns = [
    path('ws/chats/<chat_id>/', MessagesConsumer.as_asgi()),
    path('ws/chats/', ChatListConsumer.as_asgi()),
]