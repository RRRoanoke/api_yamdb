import django_filters

from django.shortcuts import get_object_or_404
from reviews.models import Genre, Title


class MyTitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')

