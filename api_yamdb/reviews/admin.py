from django.contrib import admin

from .models import Titles, Genres, Categories, Review, Comment, User

admin.site.register(User)
admin.site.register(Titles)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(Comment)
