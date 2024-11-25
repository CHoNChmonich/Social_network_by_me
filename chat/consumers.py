import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Присоединение к группе чата
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Отключение от группы чата
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']

        # Сохранение сообщения
        chat = await database_sync_to_async(Chat.objects.get)(id=self.chat_id)
        await database_sync_to_async(Message.objects.create)(
            chat=chat,
            sender=sender,
            content=message
        )

        # Отправка сообщения через WebSocket
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
            }
        )

    async def chat_message(self, event):
        # Отправка сообщения через WebSocket
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
