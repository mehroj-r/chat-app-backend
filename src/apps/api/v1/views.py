from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat_app.models import Chat, Message, ChatUser, Profile
from apps.api.v1.serializers import CreateMessageSerializer, ChatSerializer, MessageSerializer, UserSerializer, ChatUserSerializer, \
    ProfileSerializer


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

class ChatMembersListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer

    def get_chat_object(self, chat_id):
        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    def get_queryset(self):

        chat_id = self.kwargs['chat_id']
        chat = self.get_chat_object(chat_id)

        if not chat:
            return Chat.objects.none()

        return super().get_queryset().filter(chat=chat)

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

        ChatUser.objects.filter(chat_id=self.kwargs['chat_id'], user=request.user).update(last_read_message=queryset.last())

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            self.save_user(request, serializer)
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def save_user(request, serializer):
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return user


class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return User.objects.filter(username__icontains=query)[:10]

class GetCreateChatView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_object(self):
        user_id = self.request.data['user_id']
 
        return Chat.get_or_create(
            user1=self.request.user,
            user2=User.objects.get(id=user_id)
        )

    def put(self, request, *args, **kwargs):
        chat = self.get_object()
        serializer = self.serializer_class(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)