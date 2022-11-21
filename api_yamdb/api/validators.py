from rest_framework.serializers import ValidationError


def check_username(username):
    if username == 'me':
        raise ValidationError('использовать "me" запрещено!')
    return username