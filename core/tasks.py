from django.utils import timezone
from .models import ApiKey
from project.celery import app


@app.task
def update_api_key_status():
    expired_keys = ApiKey.objects.filter(expired_at__lt=timezone.now().date())
    expired_keys.update(is_active=False)
