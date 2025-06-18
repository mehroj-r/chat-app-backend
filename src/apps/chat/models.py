
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.account.models import User


class Chat(models.Model):

    class ChatTypeChoices(models.TextChoices):
        PRIVATE = 'PRIVATE', 'Private'
        GROUP = 'GROUP', 'Group'

    members = models.ManyToManyField(User, related_name='chats', through='ChatUser')
    name = models.CharField(max_length=100, null=True, blank=True)
    last_message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    type = models.CharField(choices=ChatTypeChoices.choices, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_or_create(cls, user1, user2):

        chat = cls.objects.filter(
            type=cls.ChatTypeChoices.PRIVATE,
            members=user1
        ).filter(members=user2).first()

        if chat:
            return chat

        # Create a new chat and chatusers
        with transaction.atomic():

            chat = cls.objects.create(
                name=user2.first_name,
                type=cls.ChatTypeChoices.PRIVATE
            )
            ChatUser.objects.bulk_create([
                ChatUser(chat=chat, user=user1),
                ChatUser(chat=chat, user=user2)
            ])

        return chat

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Message)
def update_last_message(sender, instance, created, **kwargs):

    if created:
        instance.chat.last_message = instance
        instance.chat.save()

class ChatUser(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_read_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


