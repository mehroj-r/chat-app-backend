from django.contrib.auth.models import User

from rest_framework import serializers

from chat_app.models import Message, Chat



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

    class Meta:
        model = Chat
        fields = (
            'id',
            'last_message',
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