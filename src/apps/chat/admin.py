from django.contrib import admin

from apps.chat.models import Chat, Message, ChatUser
from apps.account.models import Profile

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ChatUser)
admin.site.register(Profile)
