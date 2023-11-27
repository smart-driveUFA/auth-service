from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import TpiFactory
from core.models import TPI, ApiKey
from user_auth.factories import UserFactory


class TPIViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.api_key = ApiKey.objects.create(
            user=self.user,
            expired_at=datetime.utcnow().date() + timedelta(days=30),
        )
        self.valid_token = self.api_key.jwt_token
        self.tpi = TpiFactory(user=self.user)

    def test_list_tpi(self):
        """
        Получаем список tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        url = reverse("core:tpi-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            len(response.data) == TPI.objects.count()
        ), "Сверяем количество созданных tpi"

    def test_create_post(self):
        """
        Создание tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        url = reverse("core:tpi-list")
        data = {
            "latitude": self.tpi.latitude,
            "longitude": self.tpi.longitude,
            "direction": self.tpi.direction,
        }
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert (
            TPI.objects.filter(latitude=data["latitude"]).first().latitude
            == response.data["latitude"]
        ), "Сверяем title из БД и тела запроса"

    def test_retrieve_tpi(self):
        """
        Получение определенного tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["latitude"] == TPI.objects.filter(id=tpi.id).first().latitude
        )  # переписать

    def test_patch_tpi(self):
        """
        Частичное Обновление tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        data = {"latitude": 234.38475}
        response = self.client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        tpi.refresh_from_db()
        assert (
            tpi.latitude == data["latitude"]
        ), "Сравниваем обновленные данные c отправляемыми"

    def test_put_tpi(self):
        """
        Обновление tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        data = {"latitude": 345.8787, "longitude": 2.84598, "direction": "Vologda-Ufa"}
        response = self.client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        tpi.refresh_from_db()
        assert (
            tpi.latitude == data["latitude"]
        ), "Сравниваем обновленные данные c отправляемыми"

    def test_delete_tpi(self):
        """
        Удаление tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (
            TPI.objects.filter(id=tpi.id).exists() is False
        ), "Проверяем на наличие в бд"
