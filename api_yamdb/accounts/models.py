from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserRoles(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"
    MODERATOR = "moderator", "Moderator"


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
    )
    username = models.CharField(max_length=255, unique=True)
    confirmation_token = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        unique=True,
        editable=False,
    )
    REQUIRED_FIELDS = ['email']

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    def __str__(self):
        return self.username
