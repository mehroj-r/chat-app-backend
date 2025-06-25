import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser

from apps.chat.utils.async_utils import get_chat, create_message, update_chat_user_last_read
from core.websocket.client import WSClient


class MessagesConsumer(AsyncWebsocketConsumer):
    ws_client = WSClient(channel_layer=get_channel_layer())
    chat = None
    user = None

    async def connect(self):
        chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope.get('user')

        # Check if user is authenticated
        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)  # Unauthorized
            return

        # Check if chat exists
        try:
            self.chat = await get_chat(chat_id)

            # Add to group and accept connection
            await self.ws_client.add_to_group(f"chat_{chat_id}", self.channel_name)
            await self.accept()
        except Exception:
            await self.close(code=4002)
            return


    async def disconnect(self, close_code):
        await self.ws_client.remove_from_group(f"chat_{self.chat.id}", self.channel_name)

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

            return await self.ws_client.send_to_group(
                f"chat_{self.chat.id}", event
            )

        # Typing status
        if 'typing_status' in text_data_json:
            typing_status = text_data_json['typing_status']

            event = {
                'type': 'typing_status_handler',
                'username': self.user.username,
                'typing_status': typing_status,
            }

            return await self.ws_client.send_to_group(
                f"chat_{self.chat.id}", event
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
