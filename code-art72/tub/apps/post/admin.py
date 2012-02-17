from django.contrib import admin
from django.contrib.auth.models import User
from apps.post.models import Post
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class PostInline(admin.StackedInline):
    model = Post

class UserAdmin(UserAdmin):
    inlines = [ PostInline, ]

admin.site.register(User, UserAdmin)