from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from apps.chat.utils.async_utils import get_user_from_token


class WsAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that authenticates WebSocket connections using a JWT token
    from the 'Authorization' header (e.g., 'Bearer <token>').
    """

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'websocket':
            headers = dict(scope.get('headers', []))

            # Headers are lowercase and byte-encoded
            auth_header = headers.get(b'authorization')

            if auth_header:
                try:
                    token = auth_header.decode().split("Bearer ")[-1].strip()
                    user = await get_user_from_token(token)
                    scope['user'] = user
                except Exception:
                    scope['user'] = AnonymousUser()
            else:
                scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
