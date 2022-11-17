from django.shortcuts import get_object_or_404
from reviews.models import Titles, Genres, Categories
from rest_framework import filters, viewsets
from django_filters import rest_framework as filters
from .serializers import TitlesSerializer, CategoriesSerializer, GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    #filter_backends = (DjangoFilterBackend,)
    #filterset_fields = ('category__slug', 'genre__slug')


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

class CategoriesiewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer