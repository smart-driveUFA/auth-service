from rest_framework import serializers

from user_auth.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("username", "email", "is_active")
