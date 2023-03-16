"""Кастомная management-команда для импорта cvs файлов."""

import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Categories, Genres, Title, TitleGenres


# TODO: не забыть добавить остальные модели как будут готовы!!
# TODO: сделать экспешн менее базовым!!

class Command(BaseCommand):
    """Кастомная management-команда для импорта csv файлов."""

    def handle(self, *args, **options):

        cvs_files = {
            Categories: 'category.csv',
            Genres: 'genre.csv',
            Title: 'titles.csv',
            TitleGenres: 'genre_title.csv',
            # User: 'users.csv',
            # Review: 'review.csv',
            # Comments: 'comments.csv',
        }
        answer = input('Операция импорта сотрет данные из ваших моделей. Продолжать? (y/n)')
        if answer == 'y':
            for key in cvs_files.keys():
                key.objects.all().delete()
        else:
            self.stdout.write(f'Скрипт прерван.')
            quit()

        for model, file in cvs_files.items():
            with open(f'static/data/{file}', 'r', encoding='utf8') as f:
                cvs_rows = csv.DictReader(f, delimiter=',')
                for row in cvs_rows:
                    shallow_copy = row.copy()
                    for keys in shallow_copy.keys():
                        if 'category' in keys:
                            row['category_id'] = row.pop('category')
                    try:
                        model.objects.create(**row)
                    except Exception as e:
                        raise CommandError(
                            f'Ошибка: {e}, файл {file}, строка {row}'
                        )
            self.stdout.write(f'Таблица {model.__name__} импортирована!')
