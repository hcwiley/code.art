from django.conf.urls.defaults import *

urlpatterns = patterns('apps.oauth2_lite_client.views',
#    (r'^$', 'provider_cb'),
    (r'^(?P<slug>[^/]*)$', 'provider_cb'),
    (r'^oauth2callback$', 'provider_cb'),
)
