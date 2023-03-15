"""Эндпойнты приложения YaMDb."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='сategories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path("v1/", include(router.urls)),
]