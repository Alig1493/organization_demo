from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from warning.config import phone_validator, WarningType


class Thana(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TemporaryLocation(models.Model):
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    description = models.TextField()


class User(models.Model):
    name = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)
    family_number = models.CharField(max_length=1000, blank=True)
    thana = models.ForeignKey(Thana)
    temporary_location = models.CharField(max_length=1000, blank=True, default="")

    def __str__(self):
        return self.name


class WarningModel(models.Model):
    warning_type = models.IntegerField(choices=WarningType.CHOICES)
    value = models.IntegerField(default=1,
                                validators=[MaxValueValidator(10), MinValueValidator(1)])
    description = models.TextField()


class WarningSmsModel(models.Model):
    thana = models.ForeignKey(Thana)
    warning = models.ForeignKey(WarningModel, on_delete=models.CASCADE)


class LostModel(models.Model):
    phone = models.CharField(max_length=1000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    family = models.ManyToManyField(User, blank=True, related_name='family')
    description = models.TextField()

    def __str__(self):
        return self.user.name
