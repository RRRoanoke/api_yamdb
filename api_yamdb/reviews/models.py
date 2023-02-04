from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class Role:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


ROLE_CHOICE = (
    (Role.USER, "Пользователь"),
    (Role.MODERATOR, "Модератор"),
    (Role.ADMIN, "Администратор"),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, validators=(ASCIIUsernameValidator,)
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=True,
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=10, null=False, choices=ROLE_CHOICE, default=Role.USER
    )
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["email"]
