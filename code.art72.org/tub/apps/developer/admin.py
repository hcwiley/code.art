from django.contrib import admin
from django.contrib.auth.models import User
from apps.developer.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Developer)