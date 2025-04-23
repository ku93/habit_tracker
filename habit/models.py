from django.db import models
from django.core.validators import MaxValueValidator

from users.models import User


class Habit(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка'
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )
    frequency = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        default='daily',
        verbose_name='Периодичность'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )
    duration = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name='Время на выполнение (сек)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"
