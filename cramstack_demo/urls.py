"""cramstack_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Organization API\'s')

auth_token_patterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^jwt-token-auth/', obtain_jwt_token),
    url(r'^jwt-token-refresh/', refresh_jwt_token),
    url(r'^jwt-token-verify/', verify_jwt_token),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include(auth_token_patterns)),
    url(r'^api/organization/', include('organization.urls', namespace='organization')),
    url(r'^api/messenger/', include('bot.urls', namespace='messenger_bot')),
    url(r'^api/page/', include('page_bot.urls', namespace='page_bot')),
    url(r'^docs/$', schema_view),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
