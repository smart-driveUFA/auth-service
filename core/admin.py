from django.contrib import admin

from core.models import TPI, ApiKey, CountRequestTpi, BlackListJwt


class CountRequestTpiInline(admin.StackedInline):
    model = CountRequestTpi
    extra = 0
    readonly_fields = (
        "created_at",
        "status_yandex",
        "status_2gis",
        "status_ai",
        "data_yandex",
        "data_2gis",
        "data_ai"
    )


@admin.register(TPI)
class TPIAdmin(admin.ModelAdmin):
    list_display = ("combined_info", "user", "display_count_request_tpi", "created_at")
    inlines = (CountRequestTpiInline,)

    def combined_info(self, obj):
        return f"{obj.lat_start}/{obj.lon_start} | {obj.start}-{obj.end}-{obj.highway}"

    combined_info.short_description = "ТПИ"

    def display_count_request_tpi(self, obj):
        return obj.count_request_tpi

    display_count_request_tpi.short_description = 'Количество запросов'


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "expired_at", "created_at", "updated_at")
    readonly_fields = ("jwt_token", "is_active")


@admin.register(CountRequestTpi)
class CountRequestTpiAdmin(admin.ModelAdmin):
    list_display = ("tpi", "user", "created_at", "status_yandex", "status_2gis", "status_ai")

    def user(self, obj):
        return obj.tpi.user

    user.short_description = 'User'

    list_filter = ("created_at", "tpi", "status_yandex", "status_2gis", "status_ai")
    readonly_fields = (
        "tpi",
        "created_at",
        "data_yandex",
        "data_2gis",
        "data_ai",
        "status_yandex",
        "status_2gis",
        "status_ai"
    )


@admin.register(BlackListJwt)
class BlackListJwtAdmin(admin.ModelAdmin):
    list_display = ("jwt_token",)
    readonly_fields = ("jwt_token",)
