from rest_framework import serializers

from user_auth.serializers import UserSerializer

from .models import TPI, ApiKey


class TPISerializer(serializers.ModelSerializer):
    class Meta:
        model = TPI
        fields = ("latitude", "longitude", "direction")


class ApiKeySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ApiKey
        fields = ("user", "expired_at", "jwt_token", "is_active")
