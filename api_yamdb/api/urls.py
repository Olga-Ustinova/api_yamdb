from api.views import UserViewSet
from django.urls import include, path
from rest_framework import routers

from .views import get_token, register

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_token, name='token'),
]
