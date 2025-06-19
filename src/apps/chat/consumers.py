import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from apps.chat.utils.async_utils import (
    update_chat_user_last_read, get_chat, create_message
)

class MessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope.get('user')

        # Check if user is authenticated
        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)  # Unauthorized
            return

        # Get chat object
        try:
            self.chat = await get_chat(self.chat_id)

            # Add to group and accept connection
            await self.channel_layer.group_add(
                f"chat_{self.chat_id}", self.channel_name
            )
            await self.accept()

        except Exception as e:
            await self.close(code=4002)
            return


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            f"chat_{self.chat_id}", self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        # Regular message
        if 'text' in text_data_json:
            text = text_data_json['text']
            message = await create_message(self.chat, self.user, text)

            message_info = {
                "id": message.id,
                "sender_name": message.sender.first_name,
                "text": message.text,
                "sent_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }

            event = {
                'type': 'message_handler',
                'message': message_info,
            }

            return await self.channel_layer.group_send(
                f"chat_{self.chat_id}", event
            )

        # Typing status
        if 'typing_status' in text_data_json:
            typing_status = text_data_json['typing_status']

            event = {
                'type': 'typing_status_handler',
                'username': self.user.username,
                'typing_status': typing_status,
            }

            return await self.channel_layer.group_send(
                f"chat_{self.chat_id}", event
            )


        # Close connection if no valid message type
        return await self.close(code=4003)  # Not authenticated

    async def message_handler(self, event):

        await self.send(text_data=json.dumps({
            "message": event['message']
        }))

        await self.update_last_read_message(event['message']['id'])

    async def update_last_read_message(self, message_id):
        """Fetch the latest message and update last_read_message for the user"""

        if message_id:
            await update_chat_user_last_read(self.chat, self.user, message_id)


    async def typing_status_handler(self, event):
        """Send typing status to WebSocket"""
        await self.send(text_data=json.dumps({
            "typing_status": {
                "username": event["username"],
                "status": event["typing_status"]
            }
        }))


class ChatListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')

        # Check if user is authenticated
        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)  # Unauthorized
            return

        try:
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()

        except Exception as e:
            await self.close(code=4002)
            return

    async def disconnect(self, close_code):
        if self.user is not None:
            await self.channel_layer.group_discard(
                f"user_{self.user.id}", self.channel_name
            )

    async def chat_list_update(self, event):
        # Send the update to the WebSocket
        await self.send(text_data=json.dumps(event["message"]))