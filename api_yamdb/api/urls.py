"""Эндпойнты приложения YaMDb."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (
    send_token,
    get_jwt,
    APIUser,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
)

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/auth/signup/', send_token, name='send_token'),
    path('v1/auth/token/', get_jwt, name='get_jwt'),
    path('v1/users/me/', APIUser.as_view()),
]
