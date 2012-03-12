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
    (r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}),
    (r'^sitemap.txt$', direct_to_template, {'template':'sitemap.txt', 'mimetype':'text/plain'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^/$', 'views.home'),
    (r'^$', 'views.home'),
    (r'^login$', 'views.login'),
)
#OAtuh stuff
urlpatterns += patterns('',
#    url(r'^oauth/', include('oauth_provider.urls')),
#    url(r'^oauth/request_token/', 'apps.developer.views.auth_resquest'),
#    url(r'^oauth/authorize/', 'apps.developer.views.auth_authorization'), #this is for gets
#    url(r'^oauth/access_token/', 'apps.developer.views.auth_access'),
)

#TODO: submit a pull request to sorl thumbnail with updated django admin docs entry
#TODO: allow login via username or email
#TODO: make username and email unique check case insensitive
#TODO: figure out what characters will be allowed for usernames
#TODO: add in site domain info to email templates so activation links can go out correctly for testing
urlpatterns += patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^accounts/activate/(?P<activation_key>\w+)$',
                           activate,
                           name = 'registration_activate'),
                       url(r'^accounts/login$',
                           auth_views.login,
                           {'template_name': 'registration/login.html'},
                           name = 'auth_login'),
                       url(r'^accounts/logout$',
                           auth_views.logout,
                           {'template_name': 'registration/logged_out.html'},
                           name = 'auth_logout'),
                       url(r'^accounts/register$',
                           register,
                           {'form_class':RegistrationFormUniqueEmail},
                           name = 'registration_register'),
                       url(r'^accounts/register/complete$',
                           direct_to_template,
                           {'template': 'registration/registration_complete.html'},
                           name = 'registration_complete'),
                       )
#these forms needs to enforce the case insensitive email and username


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
    (r'^oauth/', include('apps.oauth2_lite_client.urls')),
)
