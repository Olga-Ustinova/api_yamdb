from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')
]


class User(AbstractUser):
    '''Переопределенная модель User'''
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(blank=True,)

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
