import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from core.models import ApiKey

User = get_user_model()


class SafeJWTAuthentication(BasicAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            return None

        if authorization_header.split(" ")[0] != "Bearer":
            raise exceptions.AuthenticationFailed("Предоставлен не Bearer токен")

        if len(authorization_header.split()) == 1:
            msg = _("Invalid basic header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(authorization_header.split()) > 2:
            msg = _(
                "Invalid basic header. Credentials string should not contain spaces.",
            )
            raise exceptions.AuthenticationFailed(msg)

        try:
            # Извлекаем access_token из заголовка
            access_token = authorization_header.split(" ")[1]
            payload = jwt.decode(
                access_token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            api_key = ApiKey.objects.filter(user_id=payload["user_id"]).first()
            if api_key is None or not api_key.is_active:
                raise exceptions.AuthenticationFailed(
                    "API-ключ недействителен или неактивен",
                )

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Срок действия токена доступа истек")
        except IndexError:
            raise exceptions.AuthenticationFailed("Отсутствует префикс токена")
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Недействительный токен доступа")

        # Получаем пользователя, связанного с payload
        user = User.objects.filter(id=payload["user_id"]).first()
        if user is None:
            raise exceptions.AuthenticationFailed("Пользователь не найден")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("Пользователь неактивен")

        # Возвращаем кортеж (пользователь, None), чтобы указать успешную аутентификацию
        return user, None
