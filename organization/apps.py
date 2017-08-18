from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    name = 'organization'

    def ready(self):
        from .signals import post_save_user_staff_enabler
