from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    # def ready(self):  # при работе ее дает связаться с бд выдает ошибку kombu.exceptions.OperationalError: Error 8 connecting to redis:6379. nodename nor servname provided, or not known.
    #     from core.tasks import update_api_key_status
    #     update_api_key_status.delay()
