from django.contrib.auth import get_user_model
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model


from reviews.models import (
    Review,
    Comment
)

User = get_user_model()


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
