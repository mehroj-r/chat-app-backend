from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.account.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'is_superuser', 'is_verified', 'last_login')
    list_filter = ('is_superuser',)
    search_fields = ('id', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-id',)
    fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
                "phone",
                'email',
                'is_superuser',
                'is_staff',
                'is_verified',
                'password',
                'created_at',
                'updated_at',
            )
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login', 'created_at', 'updated_at', 'password')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'username', 'bio')
    search_fields = ('user__first_name', 'user__last_name', 'username')
    ordering = ('-id',)
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'username',
                'bio',
                'avatar',
            )
        }),
    )
    readonly_fields = ('user',)