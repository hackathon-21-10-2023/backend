from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import Metric, FeedbackItem, Feedback, FeedbackForUser

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
        fields = ['title', 'description', 'id']


class FeedbackItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackItem
        fields = ['metric_title', 'text', 'score_tone', 'score_tone_as_human', 'score', 'score_as_human', 'from_user',
                  'form_user_id']
        ordering = ['form_user_id']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'to_user']

    to_user = UserSerializer(read_only=True)


class FeedbackDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['feedback_items']

    feedback_items = FeedbackItemSerializer(many=True)


class FeedbackItemCreateSerializer(serializers.Serializer):
    metric_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(min_value=1, max_value=5, required=True)


class FeedbackCreateSerializer(serializers.Serializer):
    feedback_items = FeedbackItemCreateSerializer(many=True, required=True)
    to_user_id = serializers.IntegerField(required=True)


class FeedbackForUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackForUser
        fields = ['id', 'to_user', 'created_at']

    to_user = UserSerializer(read_only=True)


class FeedbackForUserDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackForUser
        fields = ['id', 'to_user', 'feedbacks', 'created_at', 'score', 'score_as_human', 'text', 'score_tone', 'is_reviewed_by_gpt']

    to_user = UserSerializer(read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)

