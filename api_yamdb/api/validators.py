from django.core.exceptions import ValidationError
from rest_framework import serializers


def check_username(username):
    if username == 'me':
        raise serializers.ValidationError('использовать "me" запрещено!')
    return username