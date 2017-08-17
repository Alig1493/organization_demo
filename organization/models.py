from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Timestamp(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class IFrame(Timestamp):
    title = models.CharField(max_length=100)
    url = models.URLField()
    organization = models.ForeignKey('organization.Organization', related_name='organization')

    def __str__(self):
        title = ""
        if self.title:
            title = self.title
        else:
            title = self.url.title()
        return f"{title} - {self.organization.__str__()} - {self.url}"

    class Meta:
        verbose_name_plural = "IFrames"
        verbose_name = "IFrame"


class Organization(Timestamp):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(User, related_name='user', null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
