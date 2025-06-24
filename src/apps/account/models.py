from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.account import managers
from core.models import TimestampedModel, SoftDeleteModel


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel, SoftDeleteModel):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name']

    # For Django Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = managers.UserManager()

    def __str__(self):
        return self.phone


class Profile(TimestampedModel, SoftDeleteModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to="user_images", default="default.jpg", null=True)

    def __str__(self):
        return self.username
