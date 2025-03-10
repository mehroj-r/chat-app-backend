from django.contrib.auth.models import User

from rest_framework import serializers

from chat_app.models import Message, Chat, ChatUser



class CreateMessageSerializer(serializers.ModelSerializer):

    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    text = serializers.CharField()

    class Meta:
        model = Message
        fields = (
            'sender',
            'chat',
            'text',
        )


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

        if obj.type == Chat.ChatTypeChoices.PRIVATE and user:
            other_member = obj.members.exclude(id=user.id).first()
            return other_member.first_name if other_member else "Anonymous"
        return obj.name

class ChatUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = ChatUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )