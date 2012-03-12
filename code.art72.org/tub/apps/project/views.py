from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.project.models import *
from django.core.context_processors import csrf
from tub.views import common_args
from apps.project.forms import *

def project(request, id=None):
    project = None
    args = common_args(request)
    if id == '':
        project = Project.objects.all()
    else:
        project = Project.objects.get(id=id)
    if request.POST:
        print request.project
        try:
            if request.project['text']:
                form = TagForm(request.project)
                print form
                if form.is_valid():
                    print 'valid'
                    tag = form.save(commit=False)
                    tag.project += project
                    tag.save()
                    args.update({'result': 'your tag got added'})
                else:
                    args.update({'result': 'your tag did not validate...'})
        except:
            args.update({'result': 'that was bad...'})
        try:
            if request.project['url']:
                form = LinkForm(request.project)
                if form.is_valid():
                    link = form.save(commit=False)
                    link.project = project
                    link.save()
                    args.update({'result': 'your link got added'})
                else:
                    args.update({'result': 'your link did not validate...'})
        except:
                    args.update({'result': 'your link did not validate...'})
    print id == ''
    args.update({'project':project})
    if id == '':
        args.update({'tag_form':TagForm()})
        args.update({'link_form':LinkForm()})
    else:
        args.update({'tag_form':TagForm(instance=project)})
        args.update({'link_form':LinkForm(instance=project)})
    args.update(csrf(request))
    return render_to_response('project/basic.html', args)

