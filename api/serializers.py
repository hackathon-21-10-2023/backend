from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'email', 'department', 'position', 'is_intern', 'is_head', 'is_awaiting_feedback', 'feedback_viewed')
