from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import ApiKey
from user_auth.authentication import SafeJWTAuthentication
from user_auth.models import UserModel
from user_auth.serializers import UserSerializer
from core.serializers import ApiKeySerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Требует доработки
    :param request:
    :return:
    """
    User = get_user_model()
    username = request.data.get("username")
    password = request.data.get("password")

    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed("Требуется указать имя пользователя и пароль")

    user = User.objects.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed("Пользователь не найден")

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("Неверный пароль")

    serialized_user = UserSerializer(user).data

    access_token = ApiKey.objects.filter(user=user, is_active=True).first().jwt_token

    response = Response()
    response.data = {
        "access_token": access_token,
        "user": serialized_user,
    }

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({"user": serialized_user})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
def verify_token(request):
    """
    param headers: Authorization: token jwt
    return: Данные о ключе и пользователе status 200
    """
    token = request.headers.get("Authorization")
    access_token = token.split(" ")[1]
    key = get_object_or_404(ApiKey, jwt_token=access_token)
    serializer_data = ApiKeySerializer(key).data
    return Response({"data": serializer_data})
