from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from chat_app.models import Message, ChatUser


@receiver(post_save, sender=Message)
def notify_chat_list(sender, instance, created, **kwargs):
    """Send chat list updates when a new message is sent"""
    if not created:  # Only send updates for new messages
        return

    chat = instance.chat
    message_id = instance.id
    sender_name = instance.sender.first_name
    sender_username = instance.sender.username
    text = instance.text
    sent_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
    channel_layer = get_channel_layer()

    for user in chat.members.all():
        chat_user = ChatUser.objects.filter(chat=chat, user=user).first()

        if chat_user and chat_user.last_read_message:
            unread_count = Message.objects.filter(
                chat=chat, created_at__gt=chat_user.last_read_message.created_at
            ).count()
        else:
            unread_count = Message.objects.filter(chat=chat).count()

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
                },
            },
        )
