from django.conf.urls import url, include

from bot.views import Message, DummyView

urlpatterns = [
    url(r'^$', Message.as_view(), name="facebook_messages"),
    url(r'^dummy/$', DummyView.as_view(), name="unix_timestamp")
]
