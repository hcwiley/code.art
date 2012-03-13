from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from apps.post.forms import *
from apps.project.models import *
from django.core.context_processors import csrf


def common_args(request):
    """
    The common arguments for all gallery views.
    
    STATIC_URL: static url from settings
    year: the year at the time of request  
    """ 
    user = request.user if request.user.is_authenticated() else None
    developer = Developer.objects.get(user=user) if user != None else None
    args = {
                'base_template' : 'base-ajax.html' if request.is_ajax() else 'base.html',
                'developer' : developer,
                'STATIC_URL' : settings.STATIC_URL,
                'MEDIA_URL' : settings.MEDIA_URL,
                'posts' :  Post.objects.all(),
                'tags' : Tag.objects.all(),
                'user' : user,
           }
    print user
    return args

def home(request):
    args = common_args(request)
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.developer = Developer.objects.get(user=request.user)
            post.save()
            args.update({'result': 'your post got added'})
        else:
            args.update({'result': 'your post did not validate...'})
    args.update(csrf(request))
    args.update({'post_form':PostForm()})
    args.update({'projects': Project.objects.all()})
    return render_to_response('index.html', args)

def oauth_authorize(request):
    return False
 
def login(request):
     return False