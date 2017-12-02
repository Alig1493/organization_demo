from django.conf.urls import url, include

from warning.views import RegistrationView, LostView

urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(), name="user_registration"),
    url(r'^lost/$', LostView.as_view(), name="lost_alert"),
]
