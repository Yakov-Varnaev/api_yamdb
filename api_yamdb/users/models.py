import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(
        max_length=100,
        blank=True,
        null=True
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

    def is_admin(self):
        return self.role == self.UserRole.ADMIN
