import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validator_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]
    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$')]
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.TextField(max_length=256)
    slug  = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.TextField(max_length=256)
    slug  = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year  = models.IntegerField(validators=(validator_year,))
    description = models.TextField()
    genre = models.ForeignKey(
        Genres, on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('genre', 'category')

    def __str__(self):
        return self.name


class Reviews(models.Model):
    text = models.TextField()
    author  = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score  = models.IntegerField()
    pub_date  = models.DateField(auto_now_add=True)
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.CharField(
        'текст комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.username
