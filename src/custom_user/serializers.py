from rest_framework import serializers
from custom_user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "url", "email", "name", "is_active", "is_staff"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
