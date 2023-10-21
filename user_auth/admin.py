from django.contrib import admin

from user_auth.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
