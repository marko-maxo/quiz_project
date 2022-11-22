from channels.generic.websocket import AsyncWebsocketConsumer
import json
import jwt
from django.conf import settings

jwt_secret = settings.JWT_SECRET


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # print(self.scope)
        token = self.scope["cookies"]["jwt"]

        if not token:
            await self.disconnect("DISCONNECTED")
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            await self.disconnect("DISCONNECTED")

        # Individual user added for chats
        await self.channel_layer.group_add(
            f'chat-{payload["id"]}',
            self.channel_name
        )
        await self.channel_layer.group_add(
            'chat-all',
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        pass

    async def sending_a_message(self, event):
        message = event["message"]
        await self.send(json.dumps(message))
