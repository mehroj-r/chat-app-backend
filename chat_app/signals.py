from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message

@receiver(post_save, sender=Message)
def notify_chat_list(sender, instance, created, **kwargs):
    """Send chat list updates when a new message is sent"""
    chat = instance.chat
    message_id = instance.id
    sender_name = instance.sender.first_name
    sender_username = instance.sender.username
    text = instance.text
    sent_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
    unread_count = Message.objects.filter(chat=chat, is_read=False).count()
    channel_layer = get_channel_layer()

    for user in chat.members.all():
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "chat_list_update",
                "message": {
                    "id": chat.id,
                    "last_message": {
                        "id": message_id,
                        "sender_name": sender_name,
                        "sender_username": sender_username,
                        "text": text,
                        "sent_at": sent_at,
                    },
                    "type": chat.type,
                    "unread_count": unread_count,
                }
            }
        )