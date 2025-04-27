from django.core.exceptions import ValidationError

def validate_related_habit(value):
    '''Проверяет, что связанная привычка является приятной'''
    if value and not value.is_pleasant:
        raise ValidationError(
            'Связанной может быть только приятная привычка'
        )

def validate_reward_or_related(value):
    '''Проверяет, что указано только одно: вознаграждение ИЛИ связанная привычка'''
    if value.reward and value.linked_habit:
        raise ValidationError(
            'Нельзя одновременно указывать вознаграждение и связанную привычку'
        )

def validate_pleasant_habit(value):
    '''Проверяет, что у приятной привычки нет вознаграждения или связанной привычки'''
    if value.is_pleasant and (value.reward or value.linked_habit):
        raise ValidationError(
            'У приятной привычки не может быть вознаграждения или связанной привычки'
        )

def validate_periodicity(value):
    '''Проверяет, что периодичность не больше 7 дней'''
    if value > 7:
        raise ValidationError(
            'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
        )