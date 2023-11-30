import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.db import models

from user_auth.models import UserModel


class ApiKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    created_at = models.DateField("Создан", auto_now_add=True)
    updated_at = models.DateField("Обновлен", auto_now=True)
    expired_at = models.DateField("Срок годности", blank=True, null=True)
    jwt_token = models.TextField("JWT Токен", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "API Ключ"
        verbose_name_plural = "API Ключи"

    def save(self, expiration_days=None, *args, **kwargs):
        if not self.jwt_token or self.expired_at != self._get_previous_expired_at():
            self._generate_jwt_token(expiration_days=expiration_days)

        super(ApiKey, self).save(*args, **kwargs)

    def _get_previous_expired_at(self):
        if self.pk:
            return ApiKey.objects.get(pk=self.pk).expired_at
        return None

    def _generate_jwt_token(self, expiration_days=None):
        if expiration_days is None:
            timedelta_value = (self.expired_at - datetime.utcnow().date()).days
        else:
            timedelta_value = expiration_days

        expiration_time = datetime.utcnow() + timedelta(days=timedelta_value)
        access_token_payload = {
            "user_id": str(self.user.id),
            "exp": expiration_time,
            "iat": datetime.utcnow(),
        }
        access_token = jwt.encode(
            access_token_payload,
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        self.jwt_token = access_token

    def __str__(self):
        return str(self.user.username)


class TPI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")
    direction = models.TextField("Направление движения")
    created_at = models.DateField("Создан", auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Табло переменной информации"
        verbose_name_plural = "Список ТПИ"

    def __str__(self):
        return f"{self.latitude}/{self.longitude} - {self.direction}"


class CountRequestTpi(models.Model):
    tpi = models.ForeignKey(TPI, verbose_name="ТПИ", on_delete=models.CASCADE)
    time = models.DateTimeField("Время запроса", auto_now_add=True)

    class Meta:
        ordering = ("time",)
        verbose_name = "Запрос"
        verbose_name_plural = "Список запросов"

    def __str__(self):
        return f"{self.tpi} - {self.time}"
