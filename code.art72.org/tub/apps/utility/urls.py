from django.conf.urls import patterns
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('apps.utility.views',
    (r'^tag/(?P<id>[^/]+)$', 'tag'),
)
