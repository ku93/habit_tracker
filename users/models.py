from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    '''Модель пользователя'''
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Укажите электронную почту",
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        region='RU'
    )
    telegram_chat_id = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name='Telegram ID'
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар"
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user',
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
