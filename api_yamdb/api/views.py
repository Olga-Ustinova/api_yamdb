from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import AnonReadOrIsAdminOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadRequestSerialize,
    TitleWriteRequestSerialize,
)
from reviews.models import Category, Genre, Title
from users.models import User

from .permissions import IsAdmin
from .serializers import (
    RegisterDataSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
)


class TitleViewSet(ModelViewSet):
    '''Вьюсет для обьектов модели Title.'''

    queryset = Title.objects.all()
    permission_classes = (AnonReadOrIsAdminOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        '''Выбор сериализатора при безопасных и не безопасных методах'''

        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteRequestSerialize
        return TitleReadRequestSerialize


class GenreViewSet(CreateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    '''Вьюсет для обьектов модели Genre.'''

    permission_classes = (AnonReadOrIsAdminOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name')


class CategoryViewSet(CreateModelMixin,
                      DestroyModelMixin,
                      ListModelMixin,
                      GenericViewSet):
    '''Вьюсет для обьектов модели Category.'''

    permission_classes = (AnonReadOrIsAdminOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name')


class UserViewSet(viewsets.ModelViewSet):
    '''Создание пользователя'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer,
    )
    def me(self, request):
        '''Получение данных своей учетной записи'''
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request):
        '''Изменение данных своей учетной записи'''
        serializer = self.get_serializer(request.user,
                                         data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    '''Регистрация пользователя'''
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация',
        message=f'Код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    '''Получения токена'''
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
