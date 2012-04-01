from django.contrib import admin
from apps.utility.models import *

class TagInline(admin.StackedInline):
    model = Tag

class LinkInline(admin.StackedInline):
    model = Link

admin.site.register(Link)
admin.site.register(Tag)