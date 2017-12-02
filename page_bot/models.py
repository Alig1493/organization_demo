import re

from django.db import models


class PagePayloadModel(models.Model):
    object = models.CharField(max_length=50)

    def __str__(self):
        return self.object


class PageEntryModel(models.Model):
    payload_model = models.OneToOneField(PagePayloadModel, on_delete=models.CASCADE)
    recipient_id = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.payload_model.__str__()} - {self.recipient_id} - {self.time}"


class PageChangesModel(models.Model):
    page_entry = models.ForeignKey(PageEntryModel, on_delete=models.CASCADE)
    field = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.page_entry.id}-{self.field}"


class PageValueModel(models.Model):
    page_changes = models.ForeignKey(PageChangesModel, on_delete=models.CASCADE)
    verb = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    post_id = models.CharField(max_length=1000)
    published = models.IntegerField()
    created_time = models.DateTimeField()

    def __str__(self):
        return f"{self.created_time} - {self.message}"


class PageFromModel(models.Model):
    value = models.OneToOneField(PageValueModel)
    name = models.CharField(max_length=100)
    sender_id = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class PageSubscribersModel(models.Model):
    subscriber_name = models.CharField(max_length=1000, default="")
    subscriber_id = models.IntegerField()

    def __str__(self):
        return f"{self.subscriber_id} - {self.subscriber_name}"
