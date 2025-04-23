from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_related_habit, validate_reward_or_related,
    validate_pleasant_habit, validate_periodicity
)

class HabitSerializer(serializers.ModelSerializer):
    ''' Полный сериализатор для привычек с валидацией'''
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def validate(self, data):
        habit = Habit(**data)
        validate_related_habit(habit)
        validate_reward_or_related(habit)
        validate_pleasant_habit(habit)
        validate_periodicity(habit.periodicity)
        return data

class PublicHabitSerializer(serializers.ModelSerializer):
    '''Упрощенный сериализатор для публичных привычек'''
    class Meta:
        model = Habit
        fields = (
            'id', 'place', 'time', 'action',
            'periodicity', 'duration', 'is_public'
        )