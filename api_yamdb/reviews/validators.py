from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers


def validate_year(value):
    year = timezone.datetime.now().year
    if value > timezone.datetime.now().year:
        raise serializers.ValidationError(
            f'Год выпуска не может быть больше {year}'
        )
    return value


def validate_score(value):
    if value < 1  or value > 10:
        raise ValidationError(
            ('Оценка должна быть от 1 до 10'),
            params={'value': value},
        )
