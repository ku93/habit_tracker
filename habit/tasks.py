from celery import shared_task
from django.utils import timezone
from .models import Habit
import telegram
from django.conf import settings


@shared_task
def send_habit_reminders():
    now = timezone.now()
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).select_related('user')

    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    for habit in habits:
        if habit.user.telegram_chat_id:
            message = (
                f"⏰ Напоминание о привычке!\n\n"
                f"Действие: {habit.action}\n"
                f"Место: {habit.place}\n"
                f"Время: {habit.time.strftime('%H:%M')}\n"
                f"Длительность: {habit.duration} сек.\n"
            )

            if habit.reward:
                message += f"Вознаграждение: {habit.reward}\n"
            elif habit.linked_habit:
                message += f"Связанная привычка: {habit.linked_habit.action}\n"

            try:
                bot.send_message(
                    chat_id=habit.user.telegram_chat_id,
                    text=message
                )
            except telegram.error.TelegramError as e:
                print(f"Ошибка отправки сообщения: {e}")