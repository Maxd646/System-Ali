import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f"order_{self.order_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data['status']

        # Update order status in the database
        order = await self.update_order_status(status)

        # Broadcast the new status to all clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'order_status_update',
                'status': order.status
            }
        )

    async def order_status_update(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status']
        }))

    async def update_order_status(self, status):
        """ Helper function to update order status """
        order = await FoodOrdera.objects.aget(id=self.order_id)
        order.status = status
        await order.asave()
        return order
