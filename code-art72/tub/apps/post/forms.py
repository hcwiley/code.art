from django.forms import ModelForm, TextInput
from apps.post.models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('developer',)

class TagForm(ModelForm):
    class Meta:
        model = Tag
        exclude = ('post',)
        widgets = {
            'text': TextInput({'placeholder': "add your own tag here", 'tabindex':'2'}),
        }
        
class LinkForm(ModelForm):
    class Meta:
        model = Link
        exclude = ('post',)
        widgets = {
            'url': TextInput({'placeholder': "add your own link here", 'tabindex':'2'}),
        }