from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
admin.autodiscover()


urlpatterns = patterns('apps.post.views',
    (r'^(?P<id>[^/]*)$', 'post'),
)
