
from django.db import models

from apps.account.models import User
from apps.chat.choices import ChatTypeChoices, ChatRoleChoices


class Chat(models.Model):

    members = models.ManyToManyField(User, related_name='chats', through='ChatUser')
    name = models.CharField(max_length=100)
    last_message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    type = models.CharField(choices=ChatTypeChoices.choices, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text[:20]} ..." if len(self.text) > 20 else self.text

class ChatUser(models.Model):

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_read_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    role = models.CharField(choices=ChatRoleChoices.choices, default=ChatRoleChoices.MEMBER, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} in {self.chat.name} as {self.role}."


