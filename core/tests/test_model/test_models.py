from datetime import datetime, timedelta

from django.test import TestCase

from core.models import TPI, ApiKey, BlackListJwt, CountRequestTpi
from user_auth.factories import UserFactory
from core.factories import TpiFactory


class ApiKeyModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.api_key = ApiKey.objects.create(
            user=self.user,
            expired_at=datetime.utcnow().date() + timedelta(days=30),
        )

    def test_api_key_str(self):
        self.assertEqual(str(self.api_key), str(self.user.username))

    def test_api_key_jwt_token_created(self):
        self.assertIsNotNone(self.api_key.jwt_token)

    def test_api_key_expiration_date(self):
        self.assertIsNotNone(self.api_key.expired_at)

    def test_api_key_is_active_default(self):
        self.assertTrue(self.api_key.is_active)

    def test_blacklist_jwt_created_on_delete(self):
        api_key = self.api_key
        api_key.delete()
        blacklist_jwt = BlackListJwt.objects.filter(
            user=api_key.user, jwt_token=api_key.jwt_token,
        )
        self.assertTrue(blacklist_jwt.exists())


class TPIModeTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.tpi = TpiFactory(user=self.user)
        CountRequestTpi.objects.create(tpi=self.tpi)

    def test_tpi_str(self):
        expected_str = f"{self.tpi.lat_start}/{self.tpi.lon_start} | {self.tpi.start}-{self.tpi.end}-{self.tpi.highway}"
        self.assertEqual(str(self.tpi), expected_str)

    def test_tpi_created_at_auto_now_add(self):
        self.assertIsNotNone(self.tpi.created_at)

    def test_tpi_ordering(self):
        tpi1 = TpiFactory(user=self.user)
        tpi2 = TpiFactory(user=self.user)
        tpis = TPI.objects.all()
        self.assertEqual(tpis[0], self.tpi)
        self.assertEqual(tpis[1], tpi1)
        self.assertEqual(tpis[2], tpi2)

    def test_count_request_tpi(self):
        self.assertEqual(self.tpi.count_request_tpi, 1)


class CountRequestTpiTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.tpi_instance = TpiFactory(user=self.user)
        self.count_request_tpi = CountRequestTpi.objects.create(tpi=self.tpi_instance)

    def test_create_count_request_tpi(self):
        count_request = self.count_request_tpi
        self.assertEqual(count_request.tpi, self.tpi_instance)
        self.assertIsNotNone(count_request.created_at)
        self.assertIsNone(count_request.data_yandex)
        self.assertIsNone(count_request.data_2gis)
        self.assertIsNone(count_request.data_ai)
        self.assertFalse(count_request.status_yandex)
        self.assertFalse(count_request.status_2gis)
        self.assertFalse(count_request.status_ai)

    def test_save_method_updates_status_fields(self):
        # Создаем экземпляр CountRequestTpi и сохраняем его
        count_request = self.count_request_tpi

        # Проверяем, что поля статуса обновились в соответствии с данными
        self.assertEqual(count_request.status_yandex, False)
        self.assertEqual(count_request.status_2gis, False)
        self.assertEqual(count_request.status_ai, False)

        # Обновляем данные и сохраняем снова
        count_request.data_yandex = {"example": "data_yandex"}
        count_request.data_2gis = {"example": "data_2gis"}
        count_request.data_ai = {"example": "data_ai"}
        count_request.save()

        # Проверяем, что поля статуса обновились после добавления данных
        self.assertEqual(count_request.status_yandex, True)
        self.assertEqual(count_request.status_2gis, True)
        self.assertEqual(count_request.status_ai, True)

    def test_str_method_returns_correct_string_representation(self):
        # Создаем экземпляр CountRequestTpi
        count_request = self.count_request_tpi
        # Проверяем, что метод __str__ возвращает корректную строку
        expected_str = f"{self.tpi_instance} - {count_request.created_at}"
        self.assertEqual(str(count_request), expected_str)

    def test_ordering_by_created_at(self):
        count_request1 = CountRequestTpi.objects.create(tpi=self.tpi_instance)
        count_request2 = CountRequestTpi.objects.create(tpi=self.tpi_instance)

        # Проверяем, что сортировка работает корректно
        queryset = CountRequestTpi.objects.all()
        self.assertEqual(queryset[0], self.count_request_tpi)
        self.assertEqual(queryset[1], count_request1)
        self.assertEqual(queryset[2], count_request2)
