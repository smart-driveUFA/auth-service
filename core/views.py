from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import TPI, ApiKey
from core.serializers import TPISerializer
from user_auth.authentication import SafeJWTAuthentication
from user_auth.models import UserModel


class TPIViewSet(viewsets.ModelViewSet):
    queryset = TPI.objects.all()
    serializer_class = TPISerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SafeJWTAuthentication, SessionAuthentication]

    def get_queryset(self):
        token = self.request.headers.get("Authorization")
        access_token = token.split(" ")[1]
        user = get_object_or_404(UserModel, apikey__jwt_token=access_token)
        if user is not None:
            return TPI.objects.filter(user=user)
        else:
            return TPI.objects.none()

    def perform_create(self, serializer):
        token = self.request.headers.get("Authorization")
        access_token = token.split(" ")[1]
        user = get_object_or_404(UserModel, apikey__jwt_token=access_token)
        serializer.validated_data["user"] = user
        serializer.save()


class CreateTestModels(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "num_models",
                openapi.IN_QUERY,
                description="Number of test models to create",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def post(self, request):
        num_models_to_create = int(request.query_params.get("num_models", 0))

        if num_models_to_create > 0:
            for i in range(num_models_to_create):
                user = UserModel.objects.create(username=f"Test User - {i!s}")
                api_key = ApiKey.objects.create(
                    user=user, expired_at=datetime.utcnow().date() + timedelta(days=30),
                )
                tpi = TPI.objects.create(
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
            {"message": "Удалены все тестовые модели."}, status=status.HTTP_200_OK,
        )
