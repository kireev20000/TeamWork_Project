"""Настройка админ-панели приложения reviews."""

from django.contrib import admin
from .models import Categories, Genres, Title


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Genres)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name', 'year', 'category',)
    list_filter = ('name', 'year', 'category',)
    empty_value_display = '-пусто-'
