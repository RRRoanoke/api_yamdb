from django.core.management.base import BaseCommand

import pandas as pd

from reviews.models import Category, Genre, Title, TitleGenre


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        title = pd.read_csv(r'F:\Deev\api_yamdb\api_yamdb\static\data\titles.csv')
        for id, name, year, category in zip(
                title.id, title.name, title.year, title.category):
            models = Title(id=id, name=name, year=year, category=Category(pk=category))
            models.save()

        cat_file = pd.read_csv(r'F:\Deev\api_yamdb\api_yamdb\static\data\category.csv')
        for id, name, slug in zip(
                cat_file.id, cat_file.name, cat_file.slug):
            models = Category(id=id, name=name, slug=slug)
            models.save()

        genre = pd.read_csv(r'F:\Deev\api_yamdb\api_yamdb\static\data\genre.csv')
        for id, name, slug in zip(
        genre.id, genre.name, genre.slug):
            models = Genres(id=id, name=name, slug=slug)
            models.save()

        with open(r'F:\Deev\api_yamdb\api_yamdb\static\data\genre_title.csv') as file:
            genre_title = pd.read_csv(file)
            for id, title_id, genre_id in zip(genre_title.id, genre_title.title_id,
                                           genre_title.genre_id):
                models = TitleGenre(id=id, title=Title(pk=title_id), genre=Genre(pk=genre_id))
                models.save()

        genre = pd.read_csv(r'F:\Deev\api_yamdb\api_yamdb\static\data\genre.csv')
        for id, name, slug in zip(
                genre.id, genre.name, genre.slug):
            models = Genre(id=id, name=name, slug=slug)
            models.save()
