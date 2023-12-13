import os

from django.core.mail import send_mail

from core.models import ApiKey
from project.celery import app

from celery import current_task


@app.task
def send_email_successfully_create_user(email, api_key, current_date, expired_at):
    email_body = (
        f"Ваш token для работы с API Smart Drive\n"
        f"Token: {api_key}\n"
        f"Действует с {current_date} до {expired_at}"
    )
    send_mail(
        subject="Сервис Smart Drive",
        message=email_body,
        recipient_list=[email],
        from_email=os.getenv("EMAIL_HOST_USER"),
    )
    result = {"message": "succeeded completely"}
    current_task.update_state(state="SUCCESS", meta=result)
    return result


@app.task
def send_email_on_api_key_update(email, api_key, current_date, expired_at):
    email_body = (
        f"Обновили ваш token для работы с API Smart Drive\n"
        f"Token: {api_key}\n"
        f"Действует с {current_date} до {expired_at}"
    )
    send_mail(
        subject="Сервис Smart Drive",
        message=email_body,
        recipient_list=[email],
        from_email=os.getenv("EMAIL_HOST_USER"),
    )
    result = {"message": "succeeded completely"}
    current_task.update_state(state="SUCCESS", meta=result)
    return result


@app.task
def check_expired_key(expired_time, message, update=False):
    expired_keys = ApiKey.objects.filter(expired_at__lte=expired_time)
    if expired_keys.exists():
        if update:
            expired_keys.update(is_active=False)
        for key in expired_keys:
            send_mail(
                subject="Сервис Smart Drive",
                message=message,
                recipient_list=[key.user.email],
                from_email=os.getenv("EMAIL_HOST_USER"),
            )
        return {"message": "succeeded completely"}
    return {"message": "Not found expired_keys"}
