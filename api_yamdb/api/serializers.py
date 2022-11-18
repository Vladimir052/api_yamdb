import datetime
from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Categories, Genres, Reviews, Titles, User

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


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserInfoSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )
        

class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')

class RatingRelatedField(serializers.PrimaryKeyRelatedField):
    pass
    #def display_value(self, instance):
        #return 'Track: %s' % (instance.title)        


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(queryset=Genres.objects.all(), many=True, 
        read_only=True, slug_field='titles'
    )
    category = serializers.SlugRelatedField(
        slug_field='titles', queryset=Categories.objects.all()
    )

    rating = serializers.PrimaryKeyRelatedField(
        slug_field='rating', queryset=Reviews.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validator_year(value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise ValidationError
        return value


 
class ReviewsSerializer(serializers.ModelSerializer):
    #author = serializers.SlugRelatedField(
        #slug_field='username', queryset=User.objects.all(),
    #)
    class Meta:
        model = Reviews
        fields = ('text', 'author', 'score', 'pub_date')
