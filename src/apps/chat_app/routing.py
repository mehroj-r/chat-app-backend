from django.urls import path
from apps.chat_app.consumers import MessagesConsumer,ChatListConsumer


websocket_urlpatterns = [
    path('ws/chats/<chat_id>/', MessagesConsumer.as_asgi()),
    path('ws/chats/', ChatListConsumer.as_asgi()),
]
