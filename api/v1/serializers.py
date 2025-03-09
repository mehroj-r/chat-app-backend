from django.contrib.auth.models import User
from django.db import models

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

    class Meta:
        model = Chat
        fields = (
            'id',
            'last_message',
            'type',
            'display_name'
        )

    def get_display_name(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        if obj.type == 'private' and user:
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