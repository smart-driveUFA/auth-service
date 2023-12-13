from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import (
    CreateTestModels,
    DeleteAllTestModels,
    TPIViewSet,
    count_request_tpi,
    get_current_tpi,
)

app_name = "core"

urlpatterns = [
    path("create_test_models/", CreateTestModels.as_view(), name="create_test_models"),
    path(
        "delete_all_test_models/",
        DeleteAllTestModels.as_view(),
        name="delete_all_test_models",
    ),
    path("count_request_tpi/", count_request_tpi, name="count_request_tpi"),
    path("get_current_tpi/", get_current_tpi, name="get_current_tpi"),
]

router = DefaultRouter()
router.register("tpi", TPIViewSet, basename="tpi")

urlpatterns += router.urls
