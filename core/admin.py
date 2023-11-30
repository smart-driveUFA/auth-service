from django.contrib import admin

from core.models import TPI, ApiKey, CountRequestTpi


class CountRequestTpiInline(admin.TabularInline):
    model = CountRequestTpi
    extra = 0


@admin.register(TPI)
class TPIAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    inlines = (CountRequestTpiInline,)


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active")
    readonly_fields = ("jwt_token", "is_active")


@admin.register(CountRequestTpi)
class CountRequestTpiAdmin(admin.ModelAdmin):
    list_display = ("id", "tpi", "created_at")
