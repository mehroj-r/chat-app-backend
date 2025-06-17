from django.urls import path, include
from apps.api.v1.views import ChatListAPIView, SendMessageView, ChatMessagesListAPIView, CurrentUserView, \
    ChatMembersListAPIView, UserRegistrationView, UpdateProfileView, UserSearchView, GetCreateChatView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),

    path('chats/', ChatListAPIView.as_view()),
    path('chat/', GetCreateChatView.as_view()),
    path('users/search/', UserSearchView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('send/', SendMessageView.as_view()),
    path('chats/<int:chat_id>/messages', ChatMessagesListAPIView.as_view()),
    path('chats/<int:chat_id>/members', ChatMembersListAPIView.as_view()),

    path('token/', include(
        [
            path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('verify/', TokenVerifyView.as_view(), name='token_verify'),
        ]
    )),


    path('update-profile/', UpdateProfileView.as_view()),
]