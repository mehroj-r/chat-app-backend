from django.db import transaction
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.account.api.serializers import UserSerializer, ProfileSerializer
from apps.account.models import User, Profile

from core.dataclasses import SuccessResponse, ErrorResponse
from core.utils.logger import logger


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            try:
                with transaction.atomic():
                    user = self.save_user(request, serializer)
                    self.create_profile(user)
            except Exception as e:
                logger.error(f"User registration failed: {str(e)}")
                return ErrorResponse(data={"exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"User {user.id} registered successfully.")
            return SuccessResponse(data={"user": serializer.data}, status=status.HTTP_201_CREATED)

        logger.error(f"User registration failed: {serializer.errors}")
        return ErrorResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def save_user(request, serializer):
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return user

    @staticmethod
    def create_profile(user):
        return Profile.objects.create(user=user)


class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return SuccessResponse({"user": serializer.data}, status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        query = self.request.GET.get('query', '')

        if not query:
            users = User.objects.none()
        else:
            first_name_filter = Q(first_name__icontains=query)
            last_name_filter = Q(last_name__icontains=query)
            users = User.objects.filter(first_name_filter | last_name_filter)

        serializer = self.serializer_class(users, many=True)

        return SuccessResponse({"users": serializer.data}, status=status.HTTP_200_OK)


class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            logger.critical("Profile does not exist for the current user.")
            raise Profile.DoesNotExist("Profile does not exist for the current user.")

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(serializer.data, status=status.HTTP_200_OK)

        return ErrorResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)