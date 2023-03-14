"""Эндпойнты приложения YaMDb."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter() #заготовка, чтобы джанго запускался


urlpatterns = [
    path("v1/", include(router.urls)),
]