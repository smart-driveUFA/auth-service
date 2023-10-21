from django.contrib import admin

from core.models import TPI, ApiKey


@admin.register(TPI)
class TPIAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("id",)
