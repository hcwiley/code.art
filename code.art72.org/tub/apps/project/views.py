from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.project.models import *
from django.core.context_processors import csrf
from tub.views import common_args, get_form
from apps.project.forms import *

def project(request, id=None):
    project = None
    args = common_args(request)
    if id == '':
        project = Project.objects.all()
    else:
        project = Project.objects.get(id=id)
    print id == ''
    args.update({'project':project})
    if args['user']:
        project_form = get_form(request, ProjectForm, request.user)
        args.update({'project_forms':project_form})
    if id != "" and project.repos:
        repo = project.repos.all()[0]
        args['commits']  = repo.get_commits()
    args.update(csrf(request))
    return render_to_response('project/basic.html', args)

def new_project(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            request.user.developer.projects.add(project)
            project = form.save()
            return redirect('/profile/%s/projects' % request.user)