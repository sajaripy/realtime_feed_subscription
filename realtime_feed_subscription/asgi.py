"""
ASGI config for realtime_feed_subscription project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import feed_subscription.routing
from feed_subscription.routing import websocket_urlpatterns
from feed_subscription.jwt_middleware import jwt_auth_middleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime_feed_subscription.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": jwt_auth_middleware(
        URLRouter(websocket_urlpatterns)
    ),
})
