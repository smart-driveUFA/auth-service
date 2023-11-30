from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, username, password=None, email=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(
        verbose_name="Имя организации",
        max_length=20,
        unique=True,
    )
    photo = models.ImageField(
        verbose_name="Фотография",
        blank=True,
        null=True,
        upload_to="static/",
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    email = models.EmailField(
        max_length=255,
        verbose_name="Почта",
        unique=True,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ("username",)
        verbose_name = "Профиль"
        verbose_name_plural = "Список профилей"
