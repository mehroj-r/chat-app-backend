import json
from pprint import pprint

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from chat_app.models import Chat, Message


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


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Trying to connect...")
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        # Accept the connection first (Close it if auth fails later)
        print("Successfully connected")
        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            f"chat_{self.chat_id}", self.channel_name
        )

        print("Successfully disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        # Check if this is an authentication message
        if 'token' in text_data_json:
            print("Trying to authenticate ...")

            token = text_data_json['token']
            self.user = await get_user_from_token(token)

            # If authentication failed, close the connection
            if isinstance(self.user, AnonymousUser):
                print("Invalid token")
                await self.close(code=4001)
                return

            # Get chat object after successful authentication
            try:
                self.chat = await get_chat(self.chat_id)
                # Send confirmation of successful authentication

                await self.channel_layer.group_add(
                    f"chat_{self.chat_id}", self.channel_name
                )

                print("Successfully authenticated. Welcome, {}.".format(self.user.first_name))

            except Exception as e:
                print("Failed to authenticate: {}".format(e))
                await self.close(code=4002)
                return

        # Handle regular messages after authentication
        elif hasattr(self, 'user') and not isinstance(self.user, AnonymousUser):
            if 'text' in text_data_json:
                print("Handle regular message  ...")

                text = text_data_json['text']

                print(self.user)
                print(self.chat)
                print(text)

                message = await create_message(self.chat, self.user, text)

                event = {
                    'type': 'message_handler',
                    'message': message,
                }

                await self.channel_layer.group_send(
                    f"chat_{self.chat_id}", event
                )


        else:
            # If message received before authentication, close connection
            print("Deny messages before authentication")
            await self.close(code=4003)  # Not authenticated

    async def message_handler(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            "message": {
                "id": message.id,
                "sender_name": message.sender.first_name,
                "sender_username": message.sender.username,
                "text": message.text,
                "sent_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        }))