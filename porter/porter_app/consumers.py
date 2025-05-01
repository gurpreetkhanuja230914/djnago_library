# import json
# from channels.generic.websocket import AsyncJsonWebsocketConsumer

# class BookingStatusConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add(
#             "booking_status",self.channel_name
#         )
#         await self.accept()
#         print("websocket conection accepted")
    
#     async def disconnect(self):
#         await self.channel_layer.group_discard(
#             "booking_status",
#             self.channel_name
#         )
#         print("websocket connection disconnected")
    
#     async def receive(self, text_data):
#         data=json.loads(text_data)
#         print("received data",data)
#     async def send_booking_update(self,event):
#         booking_status=event['status']
#         await self.send(text_data=json.dumps({
#             "status":booking_status,
#         }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BookingStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f'order_{self.order_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (for debugging or further interactions)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json['status']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status
        }))

    # Method to send a message to the WebSocket when booking status is updated
    async def booking_status_update(self, event):
        status = event['status']

        # Send status to WebSocket
        await self.send(text_data=json.dumps({
            'status': status
        }))
