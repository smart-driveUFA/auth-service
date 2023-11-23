import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("proj")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
    "update-api-key-status": {
        "task": "core.tasks.update_api_key_status",
        "schedule": timedelta(hours=12),
    },
}
