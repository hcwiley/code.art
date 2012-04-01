from django.forms import ModelForm, TextInput
from apps.post.models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('developer',)
