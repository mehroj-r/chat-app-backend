from django.urls import path
from api.v1.views import ChatListAPIView, SendMessageView, ChatMessagesListAPIView, CurrentUserView, \
    ChatMembersListAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    path('chats/', ChatListAPIView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('send/', SendMessageView.as_view()),
    path('chats/<int:chat_id>/messages', ChatMessagesListAPIView.as_view()),
    path('chats/<int:chat_id>/members', ChatMembersListAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]