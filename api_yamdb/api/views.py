from django.shortcuts import get_object_or_404
from reviews.models import Titles, Genres, Categories
from rest_framework import viewsets

from .serializers import TitlesSerializer, CategoriesSerializer, GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.select_related('author')
    serializer_class = TitlesSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

class CategoriesiewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer