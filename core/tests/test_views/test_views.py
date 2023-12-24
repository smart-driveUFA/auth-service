import uuid
from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import TpiFactory
from core.models import TPI, ApiKey, CountRequestTpi
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert (
            len(response.data) == TPI.objects.filter(user=self.user).count()
        ), "Сверяем количество созданных tpi"

    def test_create_post(self):
        """
        Создание tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        url = reverse("core:tpi-list")
        data = {
            "start": "Москва",
            "end": "Уфа",
            "highway": "М5",
            "lat_start": 54.7431,
            "lon_start": 55.9678,
            "lat_end": 55.7431,
            "lon_end": 55.7432
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.data["detail"],
            "TPI created successfully"
        )  # так сделано в связи с тем что при создании обьекта респонс не отдает инстанс обьекта который был создан

    def test_retrieve_tpi(self):
        """
        Получение определенного tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["lat_start"], TPI.objects.filter(id=tpi.id).first().lat_start
        )  # переписать

    def test_patch_tpi(self):
        """
        Частичное Обновление tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        data = {"lat_start": 234.38475}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tpi.refresh_from_db()
        self.assertEqual(
            tpi.lat_start,
            data["lat_start"],
            msg="Сравниваем обновленные данные c отправляемыми"
        )

    def test_put_tpi(self):
        """
        Обновление tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        data = {
            "lat_start": 43.4732,
            "lon_start": 43.4532,
            "lat_end": 53.4732,
            "lon_end": 53.4532,
            "start": "Ufa",
            "end": "SPB",
            "highway": "M12",
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tpi.refresh_from_db()
        self.assertEqual(
            tpi.lat_start,
            data["lat_start"],
            msg="Сравниваем обновленные данные c отправляемыми"
        )

    def test_delete_tpi(self):
        """
        Удаление tpi
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        tpi = self.tpi
        url = reverse("core:tpi-detail", kwargs={"pk": tpi.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            TPI.objects.filter(id=tpi.id).exists(),
            False,
            msg="Проверяем на наличие в бд"
        )


class CountRequestTpiCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.tpi = TpiFactory(user=self.user)

    def test_create_count_request_tpi(self):

        # Подготавливаем данные для запроса
        request_data = {
            "tpi": {
                "lat_start": self.tpi.lat_start,
                "lon_start": self.tpi.lon_start,
                "start": self.tpi.start,
                "end": self.tpi.end,
                "highway": self.tpi.highway
            },
            "data_yandex": {},
            "data_2gis": {},
            "data_ai": {}
        }

        # Делаем запрос
        url = reverse("core:request_tpi")  # Замените на ваш фактический URL
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=request_data, format="json")

        # Проверяем успешность запроса и создание CountRequestTpi
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CountRequestTpi.objects.filter(tpi=self.tpi).exists())

        # Опционально: Проверяем, что статусы установлены правильно в модели CountRequestTpi
        count_request_tpi = CountRequestTpi.objects.get(tpi=self.tpi)
        self.assertFalse(count_request_tpi.status_yandex)
        self.assertFalse(count_request_tpi.status_2gis)
        self.assertFalse(count_request_tpi.status_ai)
