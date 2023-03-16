from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""
    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLE,
        default='user',
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
    )
    username = models.CharField(max_length=255, unique=True)
    bio = models.TextField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
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
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return f'{self.username}'
