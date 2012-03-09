from django.contrib import admin
from django.contrib.auth.models import User
from apps.developer.models import *
from django.contrib.auth.admin import UserAdmin

#admin.site.unregister(User)
#
#class DeveloperInline(admin.StackedInline):
#    model = Developer
#
#class UserAdmin(UserAdmin):
#    inlines = [ DeveloperInline, ]

#admin.site.register(User, UserAdmin)
admin.site.register(Developer)
admin.site.register(ExternalId)