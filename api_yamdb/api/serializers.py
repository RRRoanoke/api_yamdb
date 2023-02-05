import datetime as dt
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title, Comment, Categories, Genres, Titles
from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework.validators import UniqueValidator

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

        
class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z",
        required=True,
        validators=(ASCIIUsernameValidator,),
        max_length=150,
    )

    def validate(self, attrs):
        if attrs["username"] == "me":
            raise ValidationError("Нельзя me для username")
        return attrs


class TokenSeriliazer(serializers.Serializer):
    username = serializers.CharField(
        required=True, validators=(ASCIIUsernameValidator,)
    )
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z",
        required=True,
        validators=(
            ASCIIUsernameValidator,
            UniqueValidator(queryset=User.objects.all()),
        ),
        max_length=150,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "role",
        )


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
