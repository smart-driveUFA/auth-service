from datetime import datetime, timedelta

from django.test import TestCase

from core.models import TPI, ApiKey
from user_auth.factories import UserFactory


class ApiKeyModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.api_key = ApiKey.objects.create(
            user=self.user,
            expired_at=datetime.utcnow().date() + timedelta(days=30),
        )

    def test_api_key_str(self):
        self.assertEqual(str(self.api_key), self.user.username)

    def test_api_key_jwt_token_created(self):
        self.assertIsNotNone(self.api_key.jwt_token)

    def test_api_key_expiration_date(self):
        self.assertIsNotNone(self.api_key.expired_at)

    def test_api_key_is_active_default(self):
        self.assertTrue(self.api_key.is_active)


class TPIModeTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.tpi = TPI.objects.create(
            user=self.user,
            latitude=1.234,
            longitude=5.678,
            direction="north",
        )

    def test_tpi_str(self):
        expected_str = (
            f"{self.tpi.latitude}/{self.tpi.longitude} - {self.tpi.direction}"
        )
        self.assertEqual(str(self.tpi), expected_str)

    def test_tpi_created_at_auto_now_add(self):
        self.assertIsNotNone(self.tpi.created_at)

    def test_tpi_ordering(self):
        tpi1 = TPI.objects.create(
            user=self.user,
            latitude=2.345,
            longitude=6.789,
            direction="south",
        )
        tpi2 = TPI.objects.create(
            user=self.user,
            latitude=3.456,
            longitude=7.891,
            direction="east",
        )
        tpis = TPI.objects.all()
        self.assertEqual(tpis[0], self.tpi)
        self.assertEqual(tpis[1], tpi1)
        self.assertEqual(tpis[2], tpi2)
