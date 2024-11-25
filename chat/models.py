from django.db import models
from users.models import User

class Chat(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # Название беседы (для групповых чатов)
    participants = models.ManyToManyField(User, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Для сортировки по последнему сообщению

    def last_message(self):
        return self.messages.order_by('-created_at').first()

    def __str__(self):
        if self.name:
            return self.name
        return f"Chat between: {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}: {self.content[:20]}"
