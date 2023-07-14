from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)


class User(AbstractUser):
    """Модель Пользователя."""

    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(
        unique=True, blank=False, null=False, max_length=254
    )
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, default='user'
    )
    bio = models.TextField(blank=True)
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )
    is_moderator = models.BooleanField(default=False)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.is_authenticated and self.is_moderator

    @property
    def is_user(self):
        return self.role == 'user'
