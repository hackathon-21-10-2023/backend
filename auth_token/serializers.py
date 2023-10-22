from django.contrib.auth import authenticate
from rest_framework import serializers

from api.models import User


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """

    login = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(read_only=True)
    surname = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)
    position = serializers.CharField(read_only=True)
    photo = serializers.CharField(read_only=True)
    is_intern = serializers.BooleanField(read_only=True)
    is_head = serializers.BooleanField(read_only=True)
    is_awaiting_feedback = serializers.BooleanField(read_only=True)
    feedback_viewed = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get("login", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        try:
            user = User.objects.get(
                username=email, password=password
            )  # зачем тут authenticate? у меня с ним не работает
        except User.DoesNotExist:
            raise serializers.ValidationError("A user with this email and password was not found.")
        # user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("A user with this email and password was not found.")

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        return {
            "token": user.token,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "department": user.department,
            "position": user.position,
            "photo": user.photo,
            "is_intern": user.is_intern,
            "is_head": user.is_head,
            "is_awaiting_feedback": user.is_awaiting_feedback,
            "feedback_viewed": user.feedback_viewed,
            "id": user.id,
        }
