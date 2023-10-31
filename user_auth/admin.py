from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_auth.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    readonly_fields = ('password',)
