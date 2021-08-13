import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    bio = models.TextField(
        max_length=500,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
    )

    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            ('user', 'user'),
            ('admin', 'admin'),
            ('moderator', 'moderator'),
        ]

    role = models.CharField(
        max_length=25,
        choices=UserRole.choices,
        default='user',
    )
    confirmation_code = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
    )
