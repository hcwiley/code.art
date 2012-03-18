from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from apps.post.forms import *
from apps.project.models import *
from django.core.context_processors import csrf
from django.contrib.auth import logout#from social_auth.models import Providers

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
                'projects': Project.objects.all(),
                'user' : user,
           }
    return args

def promo(request):
    return render_to_response("promo.html")

def get_form(request, form_class, instance):
    if request.method == 'POST':
        print 'got here'
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            print 'valid'
            form.save(commit=False)
            #DO SOMETHING HERE
            form.save()
            form = form_class(instance=instance)
    else:
        form = form_class(instance=instance)
        
    return form

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
#    for p in Provider.objects.all():
#        print p
    return redirect("/auth/login/github")
 
def log_out(request):
    logout(request)
    args = common_args(request)
    return render_to_response('index.html', args)
 
def logged_in(request):
     return redirect("/profile/%s" % request.user.username)