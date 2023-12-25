import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.db import models

from user_auth.models import UserModel


class BlackListJwt(models.Model):
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    jwt_token = models.TextField("JWT Токен")
    created_at = models.DateField("Создан", auto_now_add=True)

    class Meta:
        ordering = ("id",)
        verbose_name = "API Ключ"
        verbose_name_plural = "Черный список ключей"


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

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        BlackListJwt.objects.create(user=self.user, jwt_token=self.jwt_token)

        super().delete(using, keep_parents)

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
    lat_start = models.FloatField("Широта ТПИ")
    lon_start = models.FloatField("Долгота ТПИ")
    lat_end = models.FloatField("Широта конечной точки")
    lon_end = models.FloatField("Долгота конечной точки")
    start = models.TextField("Начало трассы")
    end = models.TextField("Конец трассы")
    highway = models.TextField("Номер трассы")
    created_at = models.DateField("Создан", auto_now_add=True)
    composite_id = models.UUIDField(
        db_index=True, editable=False, null=True, blank=True,
    )

    class Meta:
        unique_together = (
            "user",
            "lat_start",
            "lon_start",
            "lat_end",
            "lon_end",
            "start",
            "end",
            "highway",
        )
        ordering = ("created_at",)
        verbose_name = "Табло переменной информации"
        verbose_name_plural = "Список ТПИ"

    @property
    def count_request_tpi(self):
        return self.countrequesttpi_set.count()

    def save(self, *args, **kwargs):
        if not self.composite_id:
            self._generate_composite_id()

        super().save(*args, **kwargs)

    def _generate_composite_id(self):
        composite_id_string = f"{self.user.username}|{self.lat_start}|{self.lon_start}|{self.start}|{self.end}|{self.highway}"

        self.composite_id = uuid.uuid5(uuid.NAMESPACE_DNS, composite_id_string)

    def __str__(self):
        return f"{self.lat_start}/{self.lon_start} | {self.start}-{self.end}-{self.highway}"


class CountRequestTpi(models.Model):
    tpi = models.ForeignKey(TPI, verbose_name="ТПИ", on_delete=models.CASCADE)
    created_at = models.DateTimeField("Время запроса", auto_now_add=True)
    data_yandex = models.JSONField("Данные ЯндексАПИ", null=True, blank=True)
    data_2gis = models.JSONField("Данные 2GIS", null=True, blank=True)
    data_ai = models.JSONField("Данные AI", null=True, blank=True)
    status_yandex = models.BooleanField("Состояние ЯндексАПИ", default=True)
    status_2gis = models.BooleanField("Состояние 2GIS", default=True)
    status_ai = models.BooleanField("Состояние AI", default=True)

    # def save(self, *args, **kwargs):
    #     self.status_yandex = self.data_yandex.get("data_yandex", None) != "None" if self.data_yandex else False
    #     self.status_2gis = self.data_2gis.get("data_2gis", None) != "None" if self.data_2gis else False
    #     self.status_ai = self.data_ai.get("data_ai", None) != "None" if self.data_ai else False
    #
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Запрос"
        verbose_name_plural = "Список запросов"

    def __str__(self):
        return f"{self.tpi} - {self.created_at}"
