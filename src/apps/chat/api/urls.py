from django.urls import path

from apps.chat.consumers import MessagesConsumer, ChatListConsumer
from .views import (
    ChatListCreateAPIView, ChatMessagesListAPIView, ChatMembersListAPIView, SendMessageView
)

app_name = "chat"
urlpatterns = [
    path('', ChatListCreateAPIView.as_view()),
    path('send/', SendMessageView.as_view()),
    path('<int:chat_id>/messages', ChatMessagesListAPIView.as_view()),
    path('<int:chat_id>/members', ChatMembersListAPIView.as_view()),
]

ws_urlpatterns = [
    path('ws/chats/<chat_id>/', MessagesConsumer.as_asgi()),
    path('ws/chats/', ChatListConsumer.as_asgi()),
]