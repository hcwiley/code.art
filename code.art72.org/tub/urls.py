from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to, direct_to_template
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth import views as auth_views
from registration.views import activate, register
from registration.forms import RegistrationFormUniqueEmail
admin.autodiscover()


urlpatterns = patterns('',
#    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^favicon.ico$', redirect_to, {'url': '/site_media/static/images/fav.ico'}),
    (r'^robots.txt$', direct_to_template, {'template':'common/robots.txt', 'mimetype':'text/plain'}),
#    (r'^sitemap.txt$', direct_to_template, {'template':'sitemap.txt', 'mimetype':'text/plain'}),
    (r'^admin/', include(admin.site.urls)),
#    (r'^/$', 'views.promo'),
    (r'^promo$', 'views.promo'),
    (r'^$', 'views.home'),
    (r'^register$', 'views.register'),
    (r'^login$', 'views.login'),
    (r'^logout$', 'views.log_out'),
    (r'^logout$', 'views.log_out'),

)


if settings.DEBUG:
    # let django serve user generated media while in development
    urlpatterns += patterns('',
#TODO don't let people name their top level series admin, site_media, etc.
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

# developer views
urlpatterns += patterns('',
    #TODO: this is a hack to allow for no slashes... dashboard urls start with slash, except for the home one
    (r'^profile/', include('apps.developer.urls')),
    (r'^post/', include('apps.post.urls')),
    (r'^project/', include('apps.project.urls')),
    (r'^auth/', include('social_auth.urls')),
    (r'^logged-in', 'views.logged_in'),
)
