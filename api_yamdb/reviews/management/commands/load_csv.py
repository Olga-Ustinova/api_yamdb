
import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from api_yamdb.settings import STATICFILES_DIRS
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)

wrong_fields = {
    'titles.csv': ('category_id', 'category'),
    'comments.csv': ('author_id', 'author'),
    'review.csv': ('author_id', 'author'),
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        def csv_to_model(csv_file, model):
            '''Читайет файлы CSV и добавляет данные в модель'''

            csv_file_path = Path(STATICFILES_DIRS[0]) / 'data' / csv_file
            with open(csv_file_path, 'r', encoding='utf-8') as data_csv_file:
                if csv_file in wrong_fields:
                    reader = csv.DictReader(data_csv_file)
                    for row in reader:
                        row[wrong_fields[csv_file][0]] = row.pop(
                            wrong_fields[csv_file][1]
                        )
                        model.objects.create(**row)
                else:
                    reader = csv.DictReader(data_csv_file)
                    for row in reader:
                        model.objects.create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                        'Данные успешно загружены из файла '
                        f'{csv_file} в модель {model.__name__}'
                    )
                )

        csv_to_model('users.csv', User)
        csv_to_model('category.csv', Category)
        csv_to_model('genre.csv', Genre)
        csv_to_model('titles.csv', Title)
        csv_to_model('genre_title.csv', GenreTitle)
        csv_to_model('review.csv', Review)
        csv_to_model('comments.csv', Comment)
