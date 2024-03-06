from django.urls import re_path
from . import consumers
# from django.conf.urls import urls

websocket_urlpatterns = [
    re_path(r'wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker', consumers.FeedConsumer.as_asgi())
]