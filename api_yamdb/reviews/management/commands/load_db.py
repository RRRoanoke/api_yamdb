from django.core.management.base import BaseCommand

import pandas as pd

from reviews.models import Categories, Genres, Titles, TitlesGenres


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        title = pd.read_csv(r'F:\Deev\api_yamdb\api_yamdb\static\data\titles.csv')
        for id, name, year, category in zip(
                title.id, title.name, title.year, title.category):
            models = Titles(id=id, name=name, year=year, category=Categories(pk=category))
            models.save()

        cat_file = pd.read_csv(r'F:\Deev\api_yamdb\api_yamdb\static\data\category.csv')
        for id, name, slug in zip(
                cat_file.id, cat_file.name, cat_file.slug):
            models = Categories(id=id, name=name, slug=slug)
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
                models = TitlesGenres(id=id, title=Titles(pk=title_id), genre=Genres(pk=genre_id))
                models.save()

        genre = pd.read_csv(r'F:\Deev\api_yamdb\api_yamdb\static\data\genre.csv')
        for id, name, slug in zip(
                genre.id, genre.name, genre.slug):
            models = Genres(id=id, name=name, slug=slug)
            models.save()
