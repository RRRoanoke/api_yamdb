from django.contrib import admin

from .models import Titles, Genres, Categories

admin.site.register(Titles)
admin.site.register(Categories)
admin.site.register(Genres)
