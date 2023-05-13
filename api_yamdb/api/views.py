from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .permissions import IsAdmin
from .serializers import (RegisterDataSerializer, TokenSerializer,
                          UserMeSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    '''Создание пользователя'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
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
