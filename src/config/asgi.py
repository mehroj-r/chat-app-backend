"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

from config.middlewares.ws_auth_middleware import WsAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()  # This sets up Django before any imports

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Import routing after Django is fully set up
from apps.chat.websocket import routing as chat_urls

django_asgi_app = get_asgi_application()

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