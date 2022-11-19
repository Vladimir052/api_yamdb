from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Comment, Genres, Reviews, Titles, User

from .mixins import (ListCreateDeleteViewSet,
                     UpdateDeleteViewSet)
from .permissions import (AdminOnly, AdminOrReadOnly,
                        OwnerAdminModeratorOrReadOnly)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          EmailSerializer, GenresSerializer, ReviewsSerializer,
                          TitlesSerializer, TokenSerializer,
                          UserInfoSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user = User.objects.create(username=username, email=email)
    token = default_token_generator.make_token(user)
    send_mail(
        subject='Ваш код для получения токена',
        message=f'Код: {token}',
        from_email='test@gmail.com',
        recipient_list=[user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserInfoSerializer
    )
    def user_info(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)


class GenresViewSet(ListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Genres.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenresSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name')


class CategoriesViewSet(ListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name')


class ReviewsViewSet(UpdateDeleteViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    

class CommentViewSet(UpdateDeleteViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
