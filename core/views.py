import uuid
from datetime import datetime, timedelta

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import TPI, ApiKey, CountRequestTpi
from core.serializers import TPISerializer, CountRequestTpiSerializer, TpiRequestSerializer
from core.utils import mixin_tpi_model
from user_auth.authentication import SafeJWTAuthentication
from user_auth.models import UserModel


class TPIViewSet(viewsets.ModelViewSet):
    queryset = TPI.objects.all()
    serializer_class = TPISerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication, SessionAuthentication)

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

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = TPISerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = mixin_tpi_model(
                create=True, get=False, data=serializer.data, user=user,
            )
            if data.get("message", None):
                return Response({"detail": data["message"]}, status.HTTP_201_CREATED)
            elif data.get("error", None):
                if "already exists" in data["error"]:
                    error_message = "provided tpi already exists"
                else:
                    error_message = data.get("error")
                return Response({"detail": error_message}, status.HTTP_400_BAD_REQUEST)


class CountRequestTpiCreateAPIView(generics.CreateAPIView):
    queryset = CountRequestTpi.objects.all()
    serializer_class = CountRequestTpiSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (SafeJWTAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.validated_data["data_yandex"] = self.request.data.get("weather", None)
        serializer.validated_data["data_2gis"] = self.request.data.get("traffic_jams_status", None)
        serializer.validated_data["data_ai"] = self.request.data.get("recommended_information", None)
        serializer.save(tpi=self.get_tpi_instance())

    def get_tpi_instance(self):
        tpi_data = self.request.data.get("tpi", {})
        serializer = TpiRequestSerializer(data=tpi_data)

        if serializer.is_valid(raise_exception=True):
            lat_start = serializer.validated_data.get("lat_start")
            lon_start = serializer.validated_data.get("lon_start")
            start = serializer.validated_data.get("start")
            end = serializer.validated_data.get("end")
            highway = serializer.validated_data.get("highway")

            composite_id_string = f"{self.request.user.username}|{lat_start}|{lon_start}|{start}|{end}|{highway}"

            composite_id = uuid.uuid5(uuid.NAMESPACE_DNS, composite_id_string)

            tpi = get_object_or_404(TPI, composite_id=composite_id)

            return tpi


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
    none_value = "None"
    if data_yandex == none_value:
        data_yandex = None
    if data_2gis == none_value:
        data_2gis = None
    if data_ai == none_value:
        data_ai = None
    if isinstance(lat, (float, int)) and isinstance(lon, (float, int)):
        tpi_exists = TPI.objects.filter(
            user=user, lat_start=lat, lon_start=lon
        ).exists()
        if tpi_exists:
            tpi_instance = TPI.objects.filter(
                user=user,
                lat_start=lat,
                lon_start=lon,
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
def get_current_tpi(request):
    user = request.user
    serializer = TpiRequestSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = mixin_tpi_model(create=False, get=True, data=serializer.data, user=user)
        if isinstance(data, dict):
            if data.get("error", None):
                return Response({"detail": data["error"]}, status.HTTP_400_BAD_REQUEST)

        elif isinstance(data, TPI):
            return Response(TPISerializer(data).data, status.HTTP_200_OK)

        else:
            return Response({"detail": "not found"}, status.HTTP_404_NOT_FOUND)


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
                    lat_start=0.0,
                    lon_start=0.0,
                    lat_end=0.0,
                    lon_end=0.0,
                    start="Москва",
                    end="Вологда",
                    highway=f"m{i}",
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
