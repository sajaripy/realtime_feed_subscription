from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import websockets
from .models import UserSubscription, User
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

class FeedConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.group_name = "binance"
        user = self.scope["user"]
        if user.is_authenticated:
            try:
                is_subscribe = await self.get_user_subscription(user)
                if is_subscribe:
                    await self.channel_layer.group_add(self.group_name, self.channel_name)
                    await self.channel_layer.group_send(
                        self.group_name, {"type": "send.data"}
                    )
                else:
                    await self.send_json(
                        {"msg": f"Please first subscribe {self.group_name} group"}
                    )
            except Exception as e:
                await self.send_json({"error": str(e)})
                await self.close()
        else:
            await self.send_json({"error": self.scope["error"]})
            await self.close()
    
    async def send_data(self, event):
        user = self.scope["user"]
        try:
            async with websockets.connect(
                "wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker"
            ) as ws:
                async for data in ws:
                    # user = self.scope["user"]
                    self.user_role = await sync_to_async(lambda: self.scope["session"].get('role', None))()
                    print(self.user_role)
                    # role = await self.get_user_role(user)
                    # self.user_role = await database_sync_to_async(lambda: self.scope.get('role', None))()
                    if self.user_role == 1:
                        await self.send_json({"data": data})
                    elif self.user_role == 2:
                        await self.send_json({"message": "connected"})
                    else:
                        print(self.user_role)
        except Exception as e:
            await self.send_json({"error": str(e)})

    async def receive_json(self, content, **kwargs):
        msg = content.get("message")
        if msg:
            self.send_json({"received_msg": msg})

    async def disconnect(self, code):
        StopConsumer()

    @database_sync_to_async
    def get_user_subscription(self, user):
        return UserSubscription.objects.filter(gc_name=self.group_name, user=user).exists()
    
    # @database_sync_to_async
    # def get_user_role(self, user):
    #     return User.objects.filter(role=self.role, user=user)


    # async def disconnect(self, close_code):
    #     # Unsubscribe the user from the feed channel
    #     await self.channel_layer.group_discard(
    #         'feed_updates',  # Channel group name
    #         self.channel_name  # Channel name for the current connection
    #     )

    # async def receive(self, text_data):
    #     # Receive message from WebSocket
    #     # You can implement custom logic here to handle incoming messages
    #     pass

    # async def send_feed_update(self, event):
    #     # Send feed update to the WebSocket client
    #     # This method is called when a feed update event is received
    #     feed_data = event['data']

    #     # Send the feed update to the WebSocket client
    #     await self.send(text_data=json.dumps({
    #         'feed_data': feed_data
    #     }))