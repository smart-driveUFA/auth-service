import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class SafeJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        User = get_user_model()
        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            return None

        try:
            # Извлекаем access_token из заголовка
            access_token = authorization_header.split(" ")[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"])

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
        return (user, None)
