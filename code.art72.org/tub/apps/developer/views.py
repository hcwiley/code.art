from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from django.contrib.admin.models import User
from tub.views import common_args

def developer_args(request):
    args = common_args(request)
    if request.user.is_authenticated() == False:
        return redirect("/login")
    args.update({
         'developer': Developer.objects.get(user = request.user),
         'base_template': 'developer/profile_base.html',
         })
    new_providers = settings.AVAILABLE_PROVIDERS
    current_providers = {}
    if request.user.is_authenticated():
        for soc in request.user.social_auth.all():
            print soc.provider
            current_providers.update({ soc.provider  : 'providers/%s.html' % soc.provider});
            if(soc.provider in settings.AVAILABLE_PROVIDERS):
                new_providers.remove(soc.provider)
        args['new_providers'] = new_providers
        args['current_providers'] = current_providers
    return args

def profile(request, developer):
    args = developer_args(request)
    return render_to_response('developer/profile.html', args)

def profile_redirect(request):
    return redirect("/profile/%s" % (request.user.username))

def edit_repos(request, developer):
    args = developer_args(request)
    repos = request.user.developer.update_repos()
    args['repos'] = repos
    return render_to_response('developer/repos.html', args)

def edit_media(request, developer):
    args = developer_args(request)
#    media = request.user.developer.medias.all()
    media = request.user.developer.update_media()
    args['media_source'] = media
    return render_to_response('developer/media.html', args)

def edit_social(request, developer):
    args = developer_args(request)
    return render_to_response('developer/social.html', args)

def edit_projects(request, developer):
    args = developer_args(request)
    return render_to_response('developer/projects.html', args)

def edit_posts(request, developer):
    args = developer_args(request)
    return render_to_response('developer/posts.html', args)

def edit_gists(request, developer):
    args = developer_args(request)
    return render_to_response('developer/gists.html', args)
