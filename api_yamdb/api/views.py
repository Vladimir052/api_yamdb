from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet, UpdateDeleteViewSet
from .permissions import (AdminOnly, AdminOrReadOnly,
                          OwnerAdminModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailSerializer, GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          TokenSerializer, UserInfoSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'
    permission_classes = (AdminOnly,)
    queryset = User.objects.all()
    search_fields = ('username',)
    serializer_class = UserSerializer

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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('category')
    serializer_class = TitleSerializer
    filter_class = filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(ListCreateDeleteViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    queryset = Genre.objects.all()
    search_fields = ('name',)
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDeleteViewSet):
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    queryset = Category.objects.all()
    search_fields = ('name',)
    serializer_class = CategorySerializer


class ReviewViewSet(UpdateDeleteViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerAdminModeratorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(UpdateDeleteViewSet):
    permission_classes = (OwnerAdminModeratorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)