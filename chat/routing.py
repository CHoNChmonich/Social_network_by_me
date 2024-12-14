from django.urls import path

from .consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/chats/<int:chat_id>/', ChatConsumer.as_asgi()),  # WebSocket для конкретного чата
]
