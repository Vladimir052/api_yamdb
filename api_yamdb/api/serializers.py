from reviews.models import Titles, Genres, Categories, User, Reviews
from rest_framework import serializers

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

 
class ReviewsSerializer(serializers.ModelSerializer):
    #author = serializers.SlugRelatedField(
        #slug_field='username', queryset=User.objects.all(),
    #)
    class Meta:
        model = Reviews
        fields = ('text', 'author', 'score', 'pub_date')

