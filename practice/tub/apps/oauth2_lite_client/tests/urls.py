from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^example/', include('oauth2_lite_client.urls')),
)
