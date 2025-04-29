from django.core.exceptions import ValidationError

def validate_related_habit(value):
    """Проверяет, что связанная привычка является приятной"""
    if value:
        from .models import Habit
        if isinstance(value, int):
            try:
                habit = Habit.objects.get(pk=value)
            except Habit.DoesNotExist:
                raise ValidationError("Связанная привычка не существует")
        else:
            habit = value

        if not habit.is_pleasant:
            raise ValidationError("Связанной может быть только приятная привычка")


def validate_reward_or_related(habit):
    """Проверяет, что указано только одно: вознаграждение ИЛИ связанная привычка"""
    if habit.reward and habit.linked_habit_id:
        raise ValidationError(
            "Нельзя одновременно указывать вознаграждение и связанную привычку"
        )


def validate_pleasant_habit(habit):
    """Проверяет, что у приятной привычки нет вознаграждения или связанной привычки"""
    if habit.is_pleasant and (habit.reward or habit.linked_habit_id):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки"
        )


def validate_periodicity(value):
    """Проверяет, что периодичность не больше 7 дней"""
    if value > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")
