from django.contrib import admin
from django.urls import path, include

from core import urls as urls_core
from user_auth import urls as urls_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include(urls_user, namespace="core")),
    path("api/v1/", include(urls_core, namespace="user_auth")),
]
