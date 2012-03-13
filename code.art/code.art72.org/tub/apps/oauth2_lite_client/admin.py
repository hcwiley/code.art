from django.contrib import admin
from apps.oauth2_lite_client.models import *

admin.site.register(Provider)
admin.site.register(Credential)
