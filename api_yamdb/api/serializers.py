from rest_framework import serializers

from reviews.models import User
from .validators import check_username


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )

    def validate_username(self, username):
        return check_username(username)


class EmailSerializer(serializers.ModelSerializer):
    """Email serializer"""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, username):
        return check_username(username)


class ConfirmCodeSerializer(serializers.Serializer):
    """Confirmation code serializer"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserInfoSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )
