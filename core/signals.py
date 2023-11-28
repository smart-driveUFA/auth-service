from django.dispatch import receiver
from django.db.models.signals import post_save
from core.models import ApiKey
from core.tasks import send_email_successfully_create_user


@receiver(post_save, sender=ApiKey)
def send_api_key_email_on_creation(sender, instance, created, **kwargs):
    if created:
        send_email_successfully_create_user.delay(instance.user.email, instance.jwt_token)
