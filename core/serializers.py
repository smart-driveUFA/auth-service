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


class TpiRequestSerializer(serializers.Serializer):
    lat_start = serializers.FloatField()
    lon_start = serializers.FloatField()
    start = serializers.CharField()
    end = serializers.CharField()
    highway = serializers.CharField()


class CountRequestTpiSerializer(serializers.ModelSerializer):
    tpi = TpiRequestSerializer()

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
