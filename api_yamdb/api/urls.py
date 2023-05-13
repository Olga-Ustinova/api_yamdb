from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    get_token,
    register,
)

router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_token, name='token'),
]
