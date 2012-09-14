from django.contrib import admin
from django.contrib.auth.models import User
from apps.developer.models import *
from django.contrib.auth.admin import UserAdmin

#admin.site.unregister(User)

#class DeveloperInLine(admin.StackedInline):
    #model = Developer

#class UserAdmin(UserAdmin):
    #inlines = [ DeveloperInLine, ]

#admin.site.register(User, UserAdmin)

admin.site.register(Developer)
