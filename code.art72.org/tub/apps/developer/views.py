from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from django.core.context_processors import csrf
from django.contrib.admin.models import User
from django.contrib.auth.forms import UserChangeForm
from tub.views import common_args, get_form
from apps.project.forms import *
from apps.developer.forms import *

def developer_args(request, developer):
    args = common_args(request)
    args.update(csrf(request))
    developer = Developer.objects.get(user=User.objects.get(username=developer))
    args.update({
         'developer': developer,
         'base_template': 'developer/profile_base.html',
         })
    new_providers = settings.AVAILABLE_PROVIDERS
    current_providers = {}
    if request.user.is_authenticated():
        for soc in developer.user.social_auth.all():
            current_providers.update({ soc.provider  : 'providers/%s.html' % soc.provider});
            if(soc.provider in settings.AVAILABLE_PROVIDERS):
                new_providers.remove(soc.provider)
        args['new_providers'] = new_providers
        args['current_providers'] = current_providers
    return args

def profile(request, developer):
    args = developer_args(request, developer)
    args['profile_form'] = get_form(request, DeveloperForm, request.user)
    args['user_form'] = get_form(request, UserChangeForm, request.user)
    return render_to_response('developer/profile.html', args)

def profile_redirect(request):
    return redirect("/profile/%s" % (request.user.username))

def edit_repos(request, developer):
    args = developer_args(request, developer)
    try:
        repos = args['developer'].update_repos()
    except:
        repos = None
    args['repos'] = repos
    return render_to_response('developer/repos.html', args)

def edit_media(request, developer, id=None):
    args = developer_args(request, developer)
    try:
        media = args['developer'].update_media()
    except:
        media = None
#    media = request.user.developer.update_media()
    if id:
        form = ProjectForm(request.POST, instance=Project.objects.get(id=id))
        if form.is_valid():
            form.save()
        request.POST = ''
        return redirect('/profile/%s/media' % developer)
    args['media_source'] = media
    project_forms = []
    for project in args['developer'].projects.all():
        project_forms.append(get_form(request, ProjectForm, project))
    args.update({'project_forms':project_forms})
    return render_to_response('developer/media.html', args)

def edit_social(request, developer):
    args = developer_args(request, developer)
    return render_to_response('developer/social.html', args)

def edit_projects(request, developer):
    args = developer_args(request, developer)
    project_forms = []
    args.update({'project_form': ProjectForm()})
    for project in args['developer'].projects.all():
        project_forms.append(get_form(request, ProjectForm, project))
    args.update({'project_forms':project_forms})
    return render_to_response('developer/projects.html', args)

def edit_posts(request, developer):
    args = developer_args(request, developer)
    return render_to_response('developer/posts.html', args)

def edit_gists(request, developer):
    args = developer_args(request, developer)
    return render_to_response('developer/gists.html', args)