from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat_app.models import Chat, Message, ChatUser
from .serializers import CreateMessageSerializer, ChatSerializer, MessageSerializer, UserSerializer

class SendMessageView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CreateMessageSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            message = serializer.save()
            return Response({'message_id': message.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(users__user=self.request.user)


class ChatMessagesListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_chat_object(self, chat_id):
        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    def get_queryset(self):

        chat_id = self.kwargs['chat_id']
        chat = self.get_chat_object(chat_id)

        if not chat:
            return Message.objects.none()

        return Message.objects.filter(chat=chat).order_by('created_at')

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        unread_messages = queryset.filter(is_read=False).exclude(id=request.user.id)
        unread_messages.update(is_read=True)

        ChatUser.objects.filter(chat_id=self.kwargs['chat_id'], user=request.user).update(unread_message_count=0)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)