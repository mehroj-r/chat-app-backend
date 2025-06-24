from django.contrib import admin

from apps.chat.models import Chat, Message, ChatUser

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'type',
                'last_message',
            )
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'type', 'last_message')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'chat', 'created_at')
    search_fields = ('text',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': (
                'sender',
                'chat',
                'text',
            )
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'text')

@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'user', 'role', 'created_at')
    search_fields = ('chat__name', 'user__profile__username')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': (
                'chat',
                'user',
                'role',
                'last_read_message',
            )
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('chat', 'user', 'created_at', 'updated_at', 'last_read_message', 'role')
