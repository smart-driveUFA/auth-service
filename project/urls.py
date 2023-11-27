from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from core import urls as urls_core
from user_auth import urls as urls_user

# Определение схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="smartdrive162@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include(urls_user, namespace="core")),
    path("api/v1/", include(urls_core, namespace="user_auth")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
]
