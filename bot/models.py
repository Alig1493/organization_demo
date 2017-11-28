import re

from django.db import models

from bot.config import UserType


class FacebookIdModel(models.Model):

    fb_id = models.IntegerField()
    user_type = models.IntegerField(choices=UserType.CHOICES, null=True)

    def __str__(self):
        return f"{self.id} - {self.get_user_type_display()}"


class MessageDetailModel(models.Model):

    mid = models.CharField(max_length=500)
    seq = models.IntegerField()

    def __str__(self):
        return self.mid


class PayloadModel(models.Model):

    url = models.URLField()
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    sticker_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return re.split('[/&+=?]+', self.url)[4]


class AttachmentModel(models.Model):

    title = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=1000)
    message = models.OneToOneField(MessageDetailModel)
    text = models.CharField(max_length=1000, blank=True)
    payload = models.OneToOneField(PayloadModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.payload.__str__()}"


class MessengerPayloadModel(models.Model):

    object = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.id} - {self.object}"


class EntryModel(models.Model):

    fb_id = models.IntegerField()
    time = models.DateTimeField()
    messenger_payload = models.ForeignKey(MessengerPayloadModel, on_delete=models.CASCADE)

    def __str__(self):
        return (f"Facebook ID: {self.fb_id} - Time: {self.time} - "
                f"Payload Type: {self.messenger_payload.__str__()}")


class MessagingModel(models.Model):

    timestamp = models.DateTimeField()
    message = models.OneToOneField(MessageDetailModel)
    sender = models.OneToOneField(FacebookIdModel, related_name='sender')
    recipient = models.OneToOneField(FacebookIdModel, related_name='recipient')
    entry = models.ForeignKey(EntryModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sender ID: {self.sender.__str__()} - Recipient ID: {self.recipient.__str__()}-"


class DummyModel(models.Model):

    date = models.DateTimeField()
