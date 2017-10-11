from django.conf.urls import url, include

from bot.views import Message

urlpatterns = [
    url(r'^$', Message.as_view(), name="facebook_messages")
]
