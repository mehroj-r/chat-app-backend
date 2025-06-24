from django.db import transaction

from apps.chat.choices import ChatTypeChoices
from apps.chat.models import Chat, ChatUser


class ChatService:
    """
    Service class for handling chat-related operations.
    """

    @classmethod
    def get_or_create_private_chat(cls, user1, user2):
        chat = Chat.objects.filter(
            type=ChatTypeChoices.PRIVATE,
            members=user1
        ).filter(members=user2).first()

        if chat:
            return chat

        # Create a new chat and chatusers
        with transaction.atomic():
            chat = Chat.objects.create(
                name=f"{user1.first_name} & {user2.first_name}",
                type=ChatTypeChoices.PRIVATE
            )
            ChatUser.objects.bulk_create([
                ChatUser(chat=chat, user=user1),
                ChatUser(chat=chat, user=user2)
            ])

        return chat