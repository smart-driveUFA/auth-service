import uuid

from django.db import models
from user_auth.models import UserModel


class ApiKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserModel, verbose_name="Пользователь", on_delete=models.CASCADE)
    key = models.TextField('API Ключ', unique=True)
    created_at = models.DateField("Создан", auto_now_add=True)
    updated_at = models.DateField("Обновлен", auto_now=True)
    expired_at = models.DateField("Истек", auto_now=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "API Ключ"
        verbose_name_plural = "API Ключи"

    def __str__(self):
        return self.key


class TPI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, verbose_name="Пользователь", on_delete=models.CASCADE)
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    direction = models.TextField("Направление движения")
    created_at = models.DateField("Создан", auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Табло переменной информации"
        verbose_name_plural = "Список ТПИ"

    def __str__(self):
        return self.direction
