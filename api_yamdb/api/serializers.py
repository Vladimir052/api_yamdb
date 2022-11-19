import datetime
from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Categories, Comment, Genres, Reviews, Titles, User

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

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Запрещено использовать me')
        return value


class TokenSerializer(serializers.ModelSerializer):
    """Token serializer"""
    confirmation_code = serializers.CharField(max_length=50,
                                              required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)

class UserInfoSerializer(UserSerializer):
    """User info serializer"""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )
        

class GenresSerializer(serializers.ModelSerializer):
    """Genre serializer"""
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    """Categories serializer"""
    class Meta:
        model = Categories
        fields = ('name', 'slug')   


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                 'description', 'genre', 'category')


class TitlesCreateSerializer(serializers.ModelSerializer):
    """Titles create serializer"""
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        many=True, 
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )


    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    """Reviews serializer"""
    author = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(),
    )
    score = serializers.IntegerField()
    class Meta:
        model = Reviews
        fields = ('text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    class Meta:
        model = Comment
        fields = ('review', 'text', 'author', 'pub_date')
