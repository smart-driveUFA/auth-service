from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from core.models import ApiKey
from core.tasks import send_email_on_api_key


@receiver(post_save, sender=ApiKey)
def send_api_key_email_on_creation(sender, instance, created, **kwargs):
    if created:
        current_date = datetime.now().date()
        send_email_on_api_key.delay(
            email=instance.user.email,
            api_key=instance.jwt_token,
            current_date=current_date,
            expired_at=instance.expired_at,
            created=created
        )


@receiver(pre_save, sender=ApiKey)
def check_api_key_changes_before_save(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        old_instance = None

    fields_of_interest = ["expired_at", "jwt_token"]

    if old_instance:
        if any(
            getattr(old_instance, field) != getattr(instance, field)
            for field in fields_of_interest
        ):
            current_date = datetime.now().date()
            send_email_on_api_key.delay(
                email=instance.user.email,
                api_key=instance.jwt_token,
                current_date=current_date,
                expired_at=instance.expired_at
            )
