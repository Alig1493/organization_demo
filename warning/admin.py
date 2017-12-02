from django.contrib import admin

# Register your models here.
from warning.models import Thana, TemporaryLocation, User, WarningModel, WarningSmsModel, LostModel

admin.site.register(Thana)
admin.site.register(TemporaryLocation)
admin.site.register(User)
admin.site.register(WarningModel)
admin.site.register(WarningSmsModel)
admin.site.register(LostModel)
