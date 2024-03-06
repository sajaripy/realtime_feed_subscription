from channels.generic.websocket import AsyncWebsocketConsumer
import json

class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Subscribe the user to the feed channel
        await self.channel_layer.group_add(
            'feed_updates',  # Channel group name
            self.channel_name  # Channel name for the current connection
        )

    async def disconnect(self, close_code):
        # Unsubscribe the user from the feed channel
        await self.channel_layer.group_discard(
            'feed_updates',  # Channel group name
            self.channel_name  # Channel name for the current connection
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        # You can implement custom logic here to handle incoming messages
        pass

    async def send_feed_update(self, event):
        # Send feed update to the WebSocket client
        # This method is called when a feed update event is received
        feed_data = event['data']

        # Send the feed update to the WebSocket client
        await self.send(text_data=json.dumps({
            'feed_data': feed_data
        }))