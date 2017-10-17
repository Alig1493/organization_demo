from django.db import models
from bot.fields import UnixDateTimeField


# Create your models here.

class FacebookIdModel(models.Model):

    fb_id = models.IntegerField()


class MessageDetailModel(models.Model):

    mid = models.CharField(max_length=500)
    seq = models.IntegerField()
    text = models.CharField(max_length=1000)


class MessengerPayloadModel(models.Model):

    object = models.CharField(max_length=500)


class EntryModel(models.Model):

    fb_id = models.IntegerField()
    time = models.DateTimeField()
    messenger_payload = models.ForeignKey(MessengerPayloadModel, on_delete=models.CASCADE)


class MessagingModel(models.Model):

    timestamp = models.DateTimeField()
    message = models.OneToOneField(MessageDetailModel)
    sender = models.OneToOneField(FacebookIdModel, related_name='sender')
    recipient = models.OneToOneField(FacebookIdModel, related_name='recipient')
    entry = models.ForeignKey(EntryModel, on_delete=models.CASCADE)


class DummyModel(models.Model):

    date = models.DateTimeField()
