from django.urls import path

from rest_framework.routers import DefaultRouter

from core.views import TPIViewSet, CreateTestModels, DeleteAllTestModels

app_name = "core"

urlpatterns = [
    path("create_test_models/", CreateTestModels.as_view(), name="create_test_models"),
    path("delete_all_test_models/", DeleteAllTestModels.as_view(), name='delete_all_test_models'),
]

router = DefaultRouter()
router.register("tpi", TPIViewSet, basename="tpi")

urlpatterns += router.urls
