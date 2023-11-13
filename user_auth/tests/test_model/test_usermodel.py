from django.test import TestCase

from user_auth.models import UserModel


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testname",
            email="test@mail.ru",
            password="testpass",
        )
        self.super_user = UserModel.objects.create_superuser(
            username="supertestname",
            email="supertest@mail.ru",
            password="supertestpass",
        )

    def test_create_user(self):
        user = UserModel.objects.create_user(
            username="testuser",
            password="testpass",
            email="test@gmail.com",
        )
        assert user == UserModel.objects.get(username="testuser")
        assert user.email == UserModel.objects.get(email="test@gmail.com").email
        assert user.username == UserModel.objects.get(username="testuser").username

    def test_create_super_user(self):
        super_user = UserModel.objects.create_superuser(
            username="supertestuser",
            password="supertestpass",
            email="supertest@gmail.com",
        )
        assert super_user == UserModel.objects.get(username="supertestuser")
        assert (
            super_user.email == UserModel.objects.get(email="supertest@gmail.com").email
        )
        assert (
            super_user.username
            == UserModel.objects.get(username="supertestuser").username
        )

    def test_str_user(self):
        assert str(self.user) == self.user.username
