from django.conf.urls import url, include

from page_bot.views import Post

urlpatterns = [
    url(r'^$', Post.as_view(), name="facebook_posts"),
]
