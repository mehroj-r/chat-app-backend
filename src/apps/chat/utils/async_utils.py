from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from apps.chat.models import Chat, Message, ChatUser
from channels.db import database_sync_to_async

from apps.account.models import User

@database_sync_to_async
def update_chat_user_last_read(chat, user, message_id):
    chat_user = ChatUser.objects.filter(chat=chat, user=user).first()

    if chat_user:
        chat_user.last_read_message_id = message_id
        chat_user.save()


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        access_token = AccessToken(token_key)
        user_id = access_token.payload.get('user_id')

        if user_id:
            return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, User.DoesNotExist):
        pass

    return AnonymousUser()


@database_sync_to_async
def get_chat(chat_id):
    return get_object_or_404(Chat, id=chat_id)


@database_sync_to_async
def create_message(chat, user, text):
    return Message.objects.create(
        chat=chat,
        sender=user,
        text=text,
    )