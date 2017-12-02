from django.apps import AppConfig


class WarningConfig(AppConfig):
    name = 'warning'

    def ready(self):
        from .signals import post_save_lost
