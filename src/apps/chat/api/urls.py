from django.urls import path

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