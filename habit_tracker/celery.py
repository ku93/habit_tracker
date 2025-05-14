import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

app = Celery("habit_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-habit-reminders": {
        "task": "habits.tasks.send_habit_reminders",
        "schedule": 60.0,
    },
}
