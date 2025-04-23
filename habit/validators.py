from django.core.exceptions import ValidationError

def validate_related_habit(value):
    if value and not value.is_pleasant:
        raise ValidationError(
            'Связанной может быть только приятная привычка'
        )

def validate_reward_or_related(value):
    if value.reward and value.linked_habit:
        raise ValidationError(
            'Нельзя одновременно указывать вознаграждение и связанную привычку'
        )

def validate_pleasant_habit(value):
    if value.is_pleasant and (value.reward or value.linked_habit):
        raise ValidationError(
            'У приятной привычки не может быть вознаграждения или связанной привычки'
        )

def validate_periodicity(value):
    if value > 7:
        raise ValidationError(
            'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
        )