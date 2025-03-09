from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Chat(models.Model):

    class ChatTypeChoices(models.TextChoices):
        PRIVATE = 'private'
        GROUP = 'group'


    members = models.ManyToManyField(User, related_name='members', through='ChatUser')
    name = models.CharField(max_length=100, null=True, blank=True)
    last_message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    type = models.CharField(choices=ChatTypeChoices, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_or_create(cls, user1, user2):
        pass

    @property
    def display_name(self):
        if self.type == 'private' and self.members.count() == 2:
            return self.members.exclude(id=self.z.id).first().username
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    is_read = models.BooleanField(default=False)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Message)
def update_last_message(sender, instance, created, **kwargs):

    if created:
        instance.chat.last_message = instance
        instance.chat.save()



class ChatUser(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unread_message_count = models.PositiveIntegerField(default=0)
    last_read_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="user_images", default="default.jpg")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
