from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from core.models import ApiKey
from core.tasks import send_email_successfully_create_user, send_email_on_api_key_update


@receiver(post_save, sender=ApiKey)
def send_api_key_email_on_creation(sender, instance, created, **kwargs):
    if created:
        current_date = datetime.now().date()
        send_email_successfully_create_user.delay(
            instance.user.email,
            instance.jwt_token,
            current_date,
            instance.expired_at,
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
            send_email_on_api_key_update.delay(
                instance.user.email,
                instance.jwt_token,
                current_date,
                instance.expired_at,
            )
