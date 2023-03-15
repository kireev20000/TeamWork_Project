"""Сериализаторы для приложения Api."""
import datetime

from rest_framework import serializers
from reviews.models import Categories, Genres, Title
from django.contrib.auth import get_user_model


User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """GET-cериализатор для произведений."""

    category = CategoriesSerializer(many=False, read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = 'заглушка для рейтинга'

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category',
        )
        read_only_fields = (
            'id', 'name', 'year', 'description', 'genre', 'category',
        )


class TitleCRUDSerializer(serializers.ModelSerializer):
    """CRUD-cериализатор для произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего!')
        return value
