from rest_framework import serializers
from django.contrib.auth import get_user_model


from reviews.models import (
    Review,
    Comment
)

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        queryset=Review.objects.all()
    ),
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
