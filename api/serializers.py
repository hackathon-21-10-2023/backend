from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Metric, FeedbackItem, Feedback

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


class FeedbackItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackItem
        fields = ['metric_title', 'text', 'score_tone', 'score_tone_as_human', 'score', 'score_as_human', 'from_user',
                  'form_user_id']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['feedback_items', 'text', 'score', 'score_as_human']

    feedback_items = FeedbackItemSerializer(many=True)
