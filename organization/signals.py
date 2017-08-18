from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def post_save_user_staff_enabler(sender, instance, created, **kwargs):
    if created:
        instance.is_staff = True
        instance.save()
