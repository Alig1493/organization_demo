from django.conf.urls import url, include

from organization.views import IFrameListCreate, IFrameDetails

iframe_patterns = [
    url(r'^$', IFrameListCreate.as_view(), name='iframe_list_create'),
    url(r'^(?P<iframe_id>[0-9]+)/$', IFrameDetails.as_view(), name='iframe_details'),
]

urlpatterns = [
    url(r'^iframe/', include(iframe_patterns, namespace='iframe')),
]
