import os
from datetime import timedelta
from django.utils import timezone

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("proj")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True
message_expired_now = "Добрый день. Ваш ключ истек"
expired_time = timezone.now().date() + timedelta(days=7)
message_expired_7_days = f"Добрый день. Ваш токен истекает {expired_time}"
app.conf.beat_schedule = {
    "update-api-key-status_expired_now": {
        "task": "core.tasks.check_expired_key",
        "schedule": crontab(hour="7", minute="30"),
        "args": (timezone.now().date(), message_expired_now, True),
    },
    "update-api-key-status_expired_in_7_days": {
        "task": "core.tasks.check_expired_key",
        "schedule": crontab(hour="7", minute="30"),
        "args": (expired_time, message_expired_7_days),
    },
}
