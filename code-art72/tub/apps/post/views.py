from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from django.core.context_processors import csrf
from tub.views import common_args
from apps.post.forms import *

def post(request, id):
    print id
    args = common_args(request)
    post = Post.objects.get(id=id)
    if request.POST:
        print request.POST
        try:
            if request.POST['text']:
                form = TagForm(request.POST)
                print form
                if form.is_valid():
                    print 'valid'
                    tag = form.save(commit=False)
                    tag.post = post
                    tag.save()
                    args.update({'result': 'your tag got added'})
                else:
                    args.update({'result': 'your tag did not validate...'})
        except:
            args.update({'result': 'your tag did not validate...'})
        try:
            if request.POST['url']:
                form = LinkForm(request.POST)
                if form.is_valid():
                    link = form.save(commit=False)
                    link.post = post
                    link.save()
                    args.update({'result': 'your link got added'})
                else:
                    args.update({'result': 'your link did not validate...'})
        except:
                    args.update({'result': 'your link did not validate...'})
        
    args.update({'post':post})
    args.update({'tag_form':TagForm(instance=post)})
    args.update({'link_form':LinkForm(instance=post)})
    args.update(csrf(request))
    return render_to_response('post/basic.html', args)
 