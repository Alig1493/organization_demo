from django.contrib import admin

# Register your models here.
from page_bot.models import PagePayloadModel, PageEntryModel, PageChangesModel, PageValueModel, PageSubscribersModel

admin.site.register(PagePayloadModel)
admin.site.register(PageEntryModel)
admin.site.register(PageChangesModel)
admin.site.register(PageValueModel)
admin.site.register(PageSubscribersModel)
