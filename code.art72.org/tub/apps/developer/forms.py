from django.forms import ModelForm
from apps.developer.models import *

class DeveloperForm(ModelForm):
    class Meta:
        model = Developer