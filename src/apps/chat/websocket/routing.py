from django.urls import path

from apps.chat.websocket.consumers import MessagesConsumer, ChatListConsumer

ws_urlpatterns = [
    path('ws/chats/<chat_id>/', MessagesConsumer.as_asgi()),
    path('ws/chats/', ChatListConsumer.as_asgi()),
]