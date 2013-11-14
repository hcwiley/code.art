from django.conf.urls import patterns
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('apps.project.views',
    (r'^new-project$', 'new_project'),
    (r'^(?P<id>[^/]*)$', 'project'),
)
