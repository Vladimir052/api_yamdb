import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)

CSV_DOC = {
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    User: 'users.csv'

}


class Command(BaseCommand):

    help = 'Заполняет базу csv файлами'

    def handle(self, *args, **kwargs):
        for model, filename in CSV_DOC.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{filename}',
                encoding='utf-8'
            ) as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    row['category_id'] = (
                        None if 'category' not in row
                        else row.pop('category')
                    )
                    model.objects.create(**row)
