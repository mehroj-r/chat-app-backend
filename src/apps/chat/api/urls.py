from django.urls import path

from .views import (
    ChatListView, ChatCreatePrivateView, ChatCreateGroupView,
    ChatMessagesListCreateView, ChatMembersListView
)

app_name = "chat"
urlpatterns = [
    path('', ChatListView.as_view()),
    path('private/', ChatCreatePrivateView.as_view()),
    path('group/', ChatCreateGroupView.as_view()),
    path('<int:chat_id>/messages/', ChatMessagesListCreateView.as_view()),
    path('<int:chat_id>/members/', ChatMembersListView.as_view()),
]