from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from reviews.models import (
    Review,
    Title
)


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all()
    ),
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Введите значение от 1 до 10')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Отзыв уже оставлен')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review
