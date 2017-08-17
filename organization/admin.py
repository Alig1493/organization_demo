from django.contrib import admin


# Register your models here.
from organization.models import IFrame, Organization


admin.site.register(IFrame)
admin.site.register(Organization)
