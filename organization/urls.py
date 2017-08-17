from django.conf.urls import url, include
from organization.views import IFrameListCreate

urlpatterns = [
    url(r'^$', IFrameListCreate.as_view(), name='iframe_list_create'),
]

