import json

import requests
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from cramstack_demo.settings import PAGE_ACCESS_TOKEN
from warning.models import LostModel


@receiver(post_save, sender=LostModel)
def post_save_lost(sender, instance, created, **kwargs):

    # if created:
    #     instance.family.refresh_from_db()
    #     print(instance.family.all())
    #     # print(instance.user.family.all())
    #     message = f"{instance.user.name}'s family is lost.\n{instance.description}"
    #
    #     if instance.user.phone:
    #         message += f"\nContact him here:{instance.user.phone}"
    #
    #     fb_page_url = f"https://graph.facebook.com/v2.11/" \
    #                   f"feed?access_token={PAGE_ACCESS_TOKEN}&message={message}"
    #     status = requests.post(fb_page_url, headers={"Content-Type": "application/json"})
    #     print(status.json())
    pass
