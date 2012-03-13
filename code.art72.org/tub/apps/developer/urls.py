from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to, direct_to_template
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth import views as auth_views
admin.autodiscover()


urlpatterns = patterns('apps.developer.views',
#    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'profile_redirect'),
    (r'^(?P<developer>[^/]+)$', 'profile'),
    (r'^(?P<developer>[^/]+)/repos$', 'edit_repos'),
#    (r'^(?P<developer>[^/]+)/media$', 'edit_media'),
#    (r'^(?P<developer>[^/]+)/social$', 'edit_social'),
#    (r'^(?P<developer>[^/]+)/projects$', 'edit_projects'),
#    (r'^(?P<developer>[^/]+)/posts$', 'edit_posts'),
#    (r'^(?P<developer>[^/]+)/gists$', 'edit_gists'),
)