from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Habit(models.Model):
    '''Модель привычек'''
    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Раз в 2 дня'),
        (3, 'Раз в 3 дня'),
        (4, 'Раз в 4 дня'),
        (5, 'Раз в 5 дней'),
        (6, 'Раз в 6 дней'),
        (7, 'Раз в неделю'),
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
        'self', on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1, verbose_name='Периодичность'
    )
    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Вознаграждение'
    )
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name='Время на выполнение (секунды)'
    )
    is_public = models.BooleanField(
        default=False, verbose_name='Публичная привычка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}: {self.action} в {self.time} ({self.place})"
