from django.conf.urls import url
from organization.views import IFrameListCreate, IFrameDetails

urlpatterns = [
    url(r'^$', IFrameListCreate.as_view(), name='iframe_list_create'),
    url(r'^(?P<iframe_id>[0-9]+)/$', IFrameDetails.as_view()),
]

