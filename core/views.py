from datetime import datetime

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import TPI, ApiKey
from core.serializers import TPISerializer

from user_auth.models import UserModel


class TPIViewSet(viewsets.ModelViewSet):
    queryset = TPI.objects.all()
    serializer_class = TPISerializer


class CreateTestModels(APIView):
    def post(self, request):
        num_models_to_create = int(request.data.get('num_models', 0))

        if num_models_to_create <= 0:

            for i in range(num_models_to_create):
                user = UserModel.objects.create(username=f'Test User - {str(i)}')
                api_key = ApiKey.objects.create(user=user, expired_at=datetime.utcnow().date())
                tpi = TPI.objects.create(user=user, latitude=0.0, longitude=0.0, direction=f'Test Direction - {str(i)}')

            return Response(
                {'message': f'Создано {num_models_to_create} тестовых моделей.'},
                status=status.HTTP_201_CREATED
            )

        else:
            return Response({'message': f'Не передано количество тестовых моделей'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAllTestModels(APIView):
    def post(self, request):
        UserModel.objects.filter(username__startswith='Test User').delete()
        ApiKey.objects.filter(user__username__startswith='Test User').delete()
        TPI.objects.filter(user__username__startswith='Test User').delete()

        return Response({'message': 'Удалены все тестовые модели.'}, status=status.HTTP_200_OK)
