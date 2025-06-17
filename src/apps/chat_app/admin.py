from django.contrib import admin

from apps.chat_app.models import Chat, Message, ChatUser, Profile

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ChatUser)
admin.site.register(Profile)
