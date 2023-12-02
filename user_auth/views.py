from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect
from rest_framework import exceptions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import ApiKey
from user_auth.authentication import SafeJWTAuthentication
from user_auth.models import UserModel
from user_auth.serializers import UserSerializer

User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
def verify_token(request):

    return Response({"detail": "success"})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Требует доработки
    :param request:
    :return:
    """

    username = request.data.get("username")
    password = request.data.get("password")

    if (username is None) or (password is None):
        raise exceptions.NotAuthenticated(
            "Требуется указать имя пользователя и пароль",
        )

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
def create_super_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    UserModel.objects.create_superuser(username=username, email=None, password=password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/admin/")  # перенаправляем на страницу админки
    return Response(
        {"message": "Failed to create superuser"},
        status=status.HTTP_400_BAD_REQUEST,
    )
