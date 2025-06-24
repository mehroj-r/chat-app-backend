from django.db import models


class ChatTypeChoices(models.TextChoices):
    PRIVATE = 'PRIVATE', 'Private'
    GROUP = 'GROUP', 'Group'


class ChatRoleChoices(models.TextChoices):
    CREATOR = 'CREATOR', 'Creator'
    ADMIN = 'ADMIN', 'Admin'
    MEMBER = 'MEMBER', 'Member'