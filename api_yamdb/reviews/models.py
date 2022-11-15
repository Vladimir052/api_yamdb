from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]

    email = models.EmailField(('email address'), blank=False, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        )
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username