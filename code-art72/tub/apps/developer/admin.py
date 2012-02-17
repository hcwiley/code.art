from django.contrib import admin
from django.contrib.auth.models import User
from apps.developer.models import Developer
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class DeveloperInline(admin.StackedInline):
    model = Developer

class UserAdmin(UserAdmin):
    inlines = [ DeveloperInline, ]

admin.site.register(User, UserAdmin)