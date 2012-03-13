# Django settings for tub project.

import os
import sys

DEBUG = True

if len(os.listdir('/Users')) > 0:
   IS_DEV = True
else:
    IS_DEV = False

TEMPLATE_DEBUG = DEBUG

MAX_IMAGE_SIZE = (1400, 1400)

# root directories
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected-static/')
# urls
MEDIA_URL = '/site_media/media/'
STATIC_URL = '/site_media/static/'
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/profile'

ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, 'admin/')
sys.path.append(PROJECT_ROOT)
 
ADMINS = (
    ('Cole Wiley', 'cole@decode72.com'),
    ('Zack Dever', 'zack@decode72.com'),
)

MANAGERS = ADMINS
AJAX_VIEW_PREFIX = 'ajax/'
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True

SECRET_KEY = 'xx6ew5*1z2b@$9t1jx*h2qlss9t85pvsq7ce=!#z)ugc)n&t4j'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# This is the URL that will be loaded for any subdomain that is not listed
# in SUBDOMAIN_URLCONFS. If you're going use wildcard subdomains, this will
# correspond to the wildcarded subdomain. 
# For example, 'accountname.mysite.com' will load the ROOT_URLCONF, since 
# it is not defined in SUBDOMAIN_URLCONFS.
ROOT_URLCONF = 'tub.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
   "django.core.context_processors.static",
   "django.contrib.auth.context_processors.auth",
   "django.core.context_processors.debug",
   "django.core.context_processors.i18n",
   "django.core.context_processors.media",
   "django.core.context_processors.static",
   "django.contrib.messages.context_processors.messages",
   "django.core.context_processors.csrf",
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, '../templates/'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, '../static/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
#    'django.contrib.admindocs',
    # everything above needed for admin
    'django.contrib.localflavor',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.webdesign',
    'apps.contactform',
    'sorl.thumbnail',
    'south',
    'registration',
    'apps.developer',
    'apps.post',
    'oauth2app',
    'apps.project',
)

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
THUMBNAIL_DEBUG = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#AUTH_PROFILE_MODULE = "user.user" #going to be something like this

SEND_BROKEN_LINK_EMAILS = True
    
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "support@decode72.com"
EMAIL_HOST_PASSWORD = "geauxmice"

# sorl
THUMBNAIL_UPSCALE = False

try:
    from local_settings import *
except ImportError:
    pass

