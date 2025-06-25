from django.contrib.auth.base_user import AbstractBaseUser
from django.db import transaction

from apps.chat.choices import ChatTypeChoices, ChatRoleChoices
from apps.chat.models import Chat, ChatUser


class ChatService:
    """
    Service class for handling chat-related operations.
    """

    @classmethod
    def get_or_create_private_chat(cls, user1: AbstractBaseUser, user2: AbstractBaseUser) -> Chat:
        """
        Get an existing private chat between two users or create a new one if it doesn't exist.
        :param user1: The first user involved in the chat.
        :param user2: The second user involved in the chat.
        :return: The existing or newly created private chat.
        """
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

    @classmethod
    def create_group_chat(cls, name: str, member_ids: list[int], creator: AbstractBaseUser) -> Chat:
        """
        Create a group chat with the given name and members.
        :param name: The name of the group chat.
        :param member_ids: A list of user IDs to be added as members of the group chat.
        :param creator: The user who is creating the group chat.
        :return: The newly created group chat.
        """

        # Create the chat
        with transaction.atomic():

            # Create the chat object
            chat = Chat.objects.create(
                name=name,
                type=ChatTypeChoices.GROUP
            )

            # Add the creator and members to the chat
            chat_members = [ChatUser(chat=chat, user_id=member_id, role=ChatRoleChoices.MEMBER) for member_id in member_ids]
            chat_members.append(ChatUser(chat=chat, user=creator, role=ChatRoleChoices.CREATOR))

            # Bulk create ChatUser instances
            ChatUser.objects.bulk_create(
                chat_members
            )

        return chat