from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
#from apps.developer.models import *
from django.core.context_processors import csrf
from tub.views import common_args
from apps.utility.models import *
from apps.utility.forms import *

def tag(request, id):
    args = common_args(request)
    tag = Tag.objects.get(id=id)
    posts = tag.post.all()
    args.update({'posts': posts})
    args.update(csrf(request))
    return render_to_response('tag.html', args)
