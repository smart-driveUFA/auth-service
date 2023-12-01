from datetime import datetime, timedelta

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import TPI, ApiKey, CountRequestTpi
from core.serializers import TPISerializer
from user_auth.authentication import SafeJWTAuthentication
from user_auth.models import UserModel


class TPIViewSet(viewsets.ModelViewSet):
    queryset = TPI.objects.all()
    serializer_class = TPISerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication,)

    def get_queryset(self):
        user = self.request.user
        if user is not None:
            return TPI.objects.filter(user=user)
        else:
            return TPI.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data["user"] = user
        serializer.save()

    def post(self, request):
        lat_start = self.request.data.get("lat_start", None)
        lon_start = self.request.data.get("lon_start", None)
        lat_end = self.request.data.get("lat_end", None)
        lon_end = self.request.data.get("lon_end", None)
        start = self.request.data.get("start", None)
        end = self.request.data.get("end", None)
        highway = self.request.data.get("highway", None)
        if (lat_start, lon_start, start, end, highway, lat_end, lon_end) is not None:
            TPI.objects.create(
                user=self.request.user.id,
                lat_start=lat_start,
                lon_start=lon_start,
                lon_end=lon_end,
                lat_end=lat_end,
                start=start,
                end=end,
                highway=highway,
            )
            return Response({"detail": "success"}, status.HTTP_201_CREATED)
        else:
            return Response({"detail": "failed"}, status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
def count_request_tpi(request):
    lat = float(request.data.get("lat", None))
    lon = float(request.data.get("lon", None))
    data_yandex = request.data.get("weather", None)
    data_2gis = request.data.get("traffic_jams_status", None)
    data_ai = request.data.get("recommended_information", None)
    user = request.user
    if isinstance(lat, (float, int)) and isinstance(lon, (float, int)):
        tpi_exists = TPI.objects.filter(user=user, latitude=lat, longitude=lon).exists()
        if tpi_exists:
            tpi_instance = TPI.objects.filter(
                user=user,
                latitude=lat,
                longitude=lon,
            ).first()
            CountRequestTpi.objects.create(
                tpi=tpi_instance,
                data_yandex=data_yandex,
                data_2gis=data_2gis,
                data_ai=data_ai,
            )
            return Response({"detail": "success"}, status.HTTP_201_CREATED)
        else:
            return Response({"detail": "tpi not found"}, status.HTTP_404_NOT_FOUND)
    else:
        raise TypeError("expected int or float")


class CreateTestModels(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "num_models": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of test models to create",
                ),
            },
            required=["num_models"],
        ),
    )
    def post(self, request):
        num_models_to_create = int(request.data.get("num_models", 0))

        if num_models_to_create > 0:
            for i in range(num_models_to_create):
                if UserModel.objects.filter(username=f"Test User - {i!s}"):
                    break
                user = UserModel.objects.create(
                    username=f"Test User - {i!s}",
                    email=f"email{i}@mail.ru",
                )
                ApiKey.objects.create(
                    user=user,
                    expired_at=datetime.utcnow().date() + timedelta(days=30),
                )
                TPI.objects.create(
                    user=user,
                    latitude=0.0,
                    longitude=0.0,
                    direction=f"Test Direction - {i!s}",
                )

            return Response(
                {"message": f"Создано {num_models_to_create} тестовых моделей."},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {"message": "Не передано количество тестовых моделей"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteAllTestModels(APIView):
    def post(self, request):
        UserModel.objects.filter(username__startswith="Test User").delete()
        ApiKey.objects.filter(user__username__startswith="Test User").delete()
        TPI.objects.filter(user__username__startswith="Test User").delete()

        return Response(
            {"message": "Удалены все тестовые модели."},
            status=status.HTTP_200_OK,
        )
