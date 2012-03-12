from django.contrib import admin
from apps.post.models import *

class TagInline(admin.StackedInline):
    model = Tag

class LinkInline(admin.StackedInline):
    model = Link

class PostAdmin(admin.ModelAdmin):
    inlines = [ TagInline, LinkInline]
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
admin.site.register(Link)
admin.site.register(Tag)