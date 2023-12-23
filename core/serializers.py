from rest_framework import serializers

from user_auth.serializers import UserSerializer
from .models import TPI, ApiKey, CountRequestTpi


class TPISerializer(serializers.ModelSerializer):
    class Meta:
        model = TPI
        fields = (
            "lat_start",
            "lon_start",
            "start",
            "end",
            "highway",
            "lat_end",
            "lon_end",
        )


class CountRequestTpiSerializer(serializers.ModelSerializer):
    tpi = TPISerializer()

    class Meta:
        model = CountRequestTpi
        fields = (
            "tpi",
            "data_yandex",
            "data_2gis",
            "data_ai",
        )


class ApiKeySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ApiKey
        fields = ("user", "expired_at", "jwt_token", "is_active")
