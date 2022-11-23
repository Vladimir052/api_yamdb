from django.core.validators import validate_email
from rest_framework.serializers import ValidationError
from reviews.models import User


def check_username(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError('Имя уже занято.')
    if username.lower() == 'me':
        raise ValidationError('Использовать "me" запрещено!')
    if username == '':
        raise ValidationError('Обязательно введите имя.')
    return username


def check_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('Данный адрес уже зарегестрирован.')
    if email == '':
        raise ValidationError('Обязательно введите email.')
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError('Введен недопустимый email.')
    return email
