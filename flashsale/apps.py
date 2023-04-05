from django.apps import AppConfig


class FlashsaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flashsale'

    def ready(self):
        from . import redis_service
        # from .kafka import kafka_service
        # from ..kafka_consumers import kafka_message
