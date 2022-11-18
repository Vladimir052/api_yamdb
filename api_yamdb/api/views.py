import uuid

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import AdminOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination
from reviews.models import Categories, Genres, Titles, User, Reviews, Comment

from .permissions import AdminOnly
from .serializers import (CategoriesSerializer, ConfirmCodeSerializer,
                          EmailSerializer, GenresSerializer, TitlesSerializer,
                          UserInfoSerializer, UserSerializer, ReviewsSerializer, CommentSerializer)
from .utils import send_confirm_code

from .mixins import (ListCreateDeleteViewSet, UpdateDeleteViewSet,
                     ListRetriveCreateDeleteViewSet)

@api_view(['POST'])
def confirmation_code(request):
    """Send confirmation_code by email"""
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email)
        send_confirm_code(user.email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username, email=email)
    send_confirm_code(user.email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Check confirmation_code and send JWT-token"""
    serializer = ConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data['confirmation_code']
    uuid_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, user.email))
    if uuid_code == confirmation_code:
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)

class GenresViewSet(ListCreateDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name')

class CategoriesViewSet(ListCreateDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name')

class ReviewsViewSet(UpdateDeleteViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

class CommentViewSet(UpdateDeleteViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer