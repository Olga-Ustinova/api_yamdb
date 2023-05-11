from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet

from api.filters import TitleFilter
from api.permissions import AnonReadOnly, IsSuperUserOrIsAdminOnly
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleGetRequestSerialize,
                             TitleRequestSerialize)
from reviews.models import Category, Genre, Title


class TitleViewSet(ModelViewSet):
    '''Вьюсет для обьектов модели Title.'''

    queryset = Title.objects.all()
    permission_classes = (AnonReadOnly | IsSuperUserOrIsAdminOnly,)
    serializer_class = TitleGetRequestSerialize
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        '''Выбор сериализатора при безопасных и не безопасных методах'''

        if self.request.method in ('POST', 'PATCH'):
            return TitleRequestSerialize
        return TitleGetRequestSerialize


class GenreViewSet(CreateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    '''Вьюсет для обьектов модели Genre.'''

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

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name')
