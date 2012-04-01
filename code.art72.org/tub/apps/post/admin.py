from django.contrib import admin
from apps.post.models import *

class PostAdmin(admin.ModelAdmin):
#    inlines = [ TagInline, LinkInline]
    class Meta:
        model = Post

admin.site.register(Post)
