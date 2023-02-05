from rest_framework import serializers

import datetime as dt

from reviews.models import Categories, Genres, Titles


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.CharField()

    class Meta:
        fields = '__all__'
        model = Categories


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres


class TitleSafeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Categories.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         many=True,
                                         queryset=Genres.objects.all())

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Неправильный год выпуска')
        return value

    class Meta:
        fields = '__all__'
        model = Titles
