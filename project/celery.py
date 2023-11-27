import datetime
import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("proj")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True
message_expired_now = "Добрый день. Ваш ключ истек"
app.conf.beat_schedule = {
    "update-api-key-status_expired_now": {
        "task": "core.tasks.check_expired_key",
        "schedule": timedelta(hours=24),
        "args": (datetime.datetime.now().date(), message_expired_now, True),
    },
}

expired_time = datetime.datetime.now().date() + timedelta(days=7)
message_expired_7_days = f"Добрый день. Ваш токен истекает {expired_time}"
app.conf.beat_schedule = {
    "update-api-key-status_expired_in_7_days": {
        "task": "core.tasks.check_expired_key",
        "schedule": timedelta(hours=24),
        "args": (expired_time, message_expired_7_days),
    },
}
