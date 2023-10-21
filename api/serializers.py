from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Metric

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'password', "last_login", "is_superuser", "first_name", "last_name", "is_staff", "is_active", "date_joined",
            "groups", "user_permissions")


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['title', 'description']
