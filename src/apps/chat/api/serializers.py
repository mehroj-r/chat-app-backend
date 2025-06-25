from rest_framework import serializers

from apps.account.api.serializers import UserSerializer
from apps.chat.choices import ChatTypeChoices
from apps.chat.models import Chat, Message, ChatUser


class CreateMessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(default=serializers.CurrentUserDefault())
    text = serializers.CharField(max_length=4096)
    chat_id = serializers.CharField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat_id', 'text', 'sender')

    def validate_chat(self, value):
        """Ensure user is a member of the chat"""
        user = self.context['request'].user

        if not value.members.filter(id=user.id).exists():
            raise serializers.ValidationError("You are not a member of this chat")

        return value

    @staticmethod
    def validate_text(value):
        """Sanitize and validate message text"""
        # Add text sanitization if needed
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")

        return value


class MessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(source='sender.first_name', read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sent_at = serializers.DateTimeField(source='created_at', format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'sender_name',
            'sender_username',
            'text',
            'sent_at',
        )


class ChatSerializer(serializers.ModelSerializer):

    last_message = MessageSerializer()
    display_name = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            'id',
            'last_message',
            'type',
            'display_name',
            'unread_count',
        )

    def get_unread_count(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        if not user:
            return 0  # Return 0 if request or user is not available

        chat_user = ChatUser.objects.filter(chat=obj, user=user).first()

        if not chat_user:
            return 0  # Return 0 if user is not part of the chat

        last_read_message = chat_user.last_read_message

        if last_read_message:
            return Message.objects.filter(chat=obj, created_at__gt=last_read_message.created_at).count()
        else:
            return Message.objects.filter(chat=obj).count()  # Count all messages if none have been read

    def get_display_name(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        if obj.type == ChatTypeChoices.PRIVATE and user:
            other_member = obj.members.exclude(id=user.id).first()
            return other_member.first_name if other_member else "Anonymous"
        return obj.name

class ChatUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.profile.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = ChatUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'role',
        )