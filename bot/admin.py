from django.contrib import admin

# Register your models here.
from bot.models import (FacebookIdModel, MessageDetailModel,
                        MessagingModel, MessengerPayloadModel,
                        EntryModel)

admin.site.register(FacebookIdModel)
admin.site.register(MessageDetailModel)
admin.site.register(MessagingModel)
admin.site.register(MessengerPayloadModel)
admin.site.register(EntryModel)
