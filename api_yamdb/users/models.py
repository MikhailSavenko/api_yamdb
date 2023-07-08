from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)


class Users(AbstractUser):
    """Модель Пользователя."""
    username = models.CharField(max_length=30, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    confirmation_code = models.CharField(max_length=10, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', blank=True)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')