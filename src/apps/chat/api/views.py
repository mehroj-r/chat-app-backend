from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.account.models import User
from apps.chat.api.serializers import ChatSerializer, ChatUserSerializer, MessageSerializer, CreateMessageSerializer
from apps.chat.models import Chat, ChatUser, Message
from core.dataclasses import SuccessResponse, ErrorResponse


class ChatListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_object(self):
        user_id = self.request.data.get('user_id', -1)

        if user_id == -1:
            raise ValueError("User ID is required to be in the body to create a chat.")

        if user_id == self.request.user.id:
            raise ValueError("You cannot create a chat with yourself.")

        return Chat.get_or_create(
            user1=self.request.user,
            user2=User.objects.get(id=user_id)
        )

    def list(self, request, *args, **kwargs):
        queryset = Chat.objects.filter(members=self.request.user)

        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse({"chats":serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            chat = self.get_object()
        except Exception as e:
            return ErrorResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not chat:
            return ErrorResponse({"message": "Chat could not be created."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(chat)
        return SuccessResponse({"chat": serializer.data}, status=status.HTTP_200_OK)

class ChatMembersListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer

    def get_object(self):
        chat_id = self.kwargs.get('chat_id', -1)

        if chat_id == -1:
            raise ValueError("Chat ID is required to get chat members.")

        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None


    def list(self, request, *args, **kwargs):

        try:
            chat = self.get_object()
        except ValueError as e:
            return ErrorResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not chat:
            chat_users = ChatUser.objects.none()
        else:
            chat_users = ChatUser.objects.filter(chat=chat)

        # If no chat found, return 404
        if not chat_users:
            return ErrorResponse({"message": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is a member of the chat
        if not chat_users.filter(user=request.user).exists():
            return ErrorResponse({"message": "You are not a member of this chat."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(chat_users, many=True)
        return SuccessResponse({"members": serializer.data}, status=status.HTTP_200_OK)

class ChatMessagesListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_object(self):

        chat_id = self.kwargs.get('chat_id', -1)

        if chat_id == -1:
            raise ValueError("Chat ID is required to get messages.")

        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):

        try:
            chat = self.get_object()
        except ValueError as e:
            return ErrorResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not chat:
            return ErrorResponse({"message": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is a member of the chat
        if not chat.members.filter(id=request.user.id).exists():
            return ErrorResponse({"message": "You are not a member of this chat."}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(chat=chat).order_by('created_at')

        serializer = self.get_serializer(messages, many=True)

        return SuccessResponse({"messages": serializer.data }, status=status.HTTP_200_OK)


class SendMessageView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CreateMessageSerializer

    def get_object(self):
        chat_id = self.request.data.get('chat_id', -1)

        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):

        try:
            chat = self.get_object()
        except ValueError as e:
            return ErrorResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not chat:
            return ErrorResponse({"message": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return SuccessResponse({'message': serializer.data}, status=status.HTTP_201_CREATED)

        return ErrorResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
