from django.forms import ModelForm
from apps.Developer.models import *

class DeveloperForm(ModelForm):
    class Meta:
        model = Developer
