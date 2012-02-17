from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *


def common_args(request):
    """
    The common arguments for all gallery views.
    
    STATIC_URL: static url from settings
    year: the year at the time of request  
    """ 
    artist = get_object_or_404(Artist, user__username=request.subdomain)
    args = {
                'base_template' : 'dashboard/base-ajax.html' if request.is_ajax() else 'dashboard/base.html',
                'developer' : developer,
                'STATIC_URL' : settings.STATIC_URL,
                'MEDIA_URL' : settings.MEDIA_URL,
                'posts' :  Post.objects.all(),
           }
    return args

def home(request):
    args = common_args(request)
    return render_to_response('index.html', args)
 