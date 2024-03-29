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
import feed_subscription.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime_feed_subscription.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            feed_subscription.routing.websocket_urlpatterns
        )
    ),
})
