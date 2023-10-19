import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, username, password=None, email=None):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(
        verbose_name="Имя организации",
        max_length=20,
        unique=True,
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    email = models.EmailField(
        max_length=50,
        verbose_name="Почта",
        unique=True,
        null=True,
        blank=True,
    )
    is_verify_email = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name="Группы",
        blank=True,
        related_name="пользователь_профили",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="Права пользователя",
        blank=True,
        related_name="пользователь_профили",
    )

    USERNAME_FIELD = "username"

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ("username",)
        verbose_name = "Профиль"
        verbose_name_plural = "Список профилей"
