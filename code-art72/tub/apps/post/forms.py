from django.forms import ModelForm
from apps.post.models import *

class PostForm(ModelForm):
    class Meta:
        model = Post

class TagForm(ModelForm):
    class Meta:
        model = Tag
        
class LinkForm(ModelForm):
    class Meta:
        model = Link
