from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q, F
from django.db.models.aggregates import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.chat.models import Message, ChatUser


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

    # Fetch all chat users with related user and last_read_message with unread_count in a single query
    chat_users = ChatUser.objects.filter(chat=chat).select_related(
        'user', 'last_read_message'
    ).annotate(
        unread_count=Count(
            'chat__messages',
            filter=Q(
                chat__messages__created_at__gt=F('last_read_message__created_at')
            ) | Q(last_read_message__isnull=True)
        )
    )

    # Send updates to all users in a single loop, using pre-calculated data
    for chat_user in chat_users:
        user_id = chat_user.user.id

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
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
                    "unread_count": chat_user.unread_count,
                },
            },
        )