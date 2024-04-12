from django.urls import re_path
from . import consumers
# from django.conf.urls import urls

websocket_urlpatterns = [
    re_path(r'ws/binance/', consumers.FeedConsumer.as_asgi())
]