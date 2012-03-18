from django.forms import ModelForm, TextInput
from apps.project.models import *

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        
class RepoForm(ModelForm):
    class Meta:
        model = Repo
        
class ExtendedImageForm(ModelForm):
    class Meta:
        model = ExtendedImage
        
class MediaForm(ModelForm):
    class Meta:
        model = Media