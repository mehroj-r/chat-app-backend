import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser

from core.websocket.client import WSClient


class ChatListConsumer(AsyncWebsocketConsumer):
    ws_client = WSClient(channel_layer=get_channel_layer())
    user = None

    async def connect(self):
        self.user = self.scope.get('user')

        # Check if user is authenticated
        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)  # Unauthorized
            return

        try:
            await self.ws_client.add_to_group(f"user_{self.user.id}", self.channel_name)
            await self.accept()

        except Exception:
            await self.close(code=4002)
            return

    async def disconnect(self, close_code):
        if self.user is not None:
            await self.ws_client.remove_from_group(f"user_{self.user.id}", self.channel_name)

    async def chat_list_update(self, event):
        # Send the update to the WebSocket
        await self.send(text_data=json.dumps(event["message"]))
