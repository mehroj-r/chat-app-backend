"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

from config.middlewares.ws_auth_middleware import WsAuthMiddleware
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Import routing after Django is fully set up
from core.websocket import routing as chat_urls

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": WsAuthMiddleware(
        AuthMiddlewareStack(
          URLRouter(
              chat_urls.ws_urlpatterns
          )
        ),
    ),
})