from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from django.core.context_processors import csrf
from tub.views import common_args
from apps.post.forms import *
from apps.utility.forms import *
from apps.utility.models import *

def list_post(request):
    args.update({'post_form':PostForm(instance = post)})
    args.update(csrf(request))
    return render_to_response('post/list.html', args)

def post(request, id):
    args = common_args(request)
    if id == '':
        return redirect('list_posts')
    post = Post.objects.get(id = id)
    if request.POST:
        print request.POST
        try:
            if request.POST['text']:
                    print request.POST
                    form = TagForm(request.POST)
                    if form.is_valid():
                        print 'valid'
                        tag = form.save()
                        print tag
                        post.tags.add(tag)
                        args.update({'result': 'your tag got added'})
                    else:
                        args.update({'result': 'your tag did not validate...'})
        except:
            args.update({'result': 'not a tag'})
            isTag = False
            try:
                if request.POST['url']:
                    form = LinkForm(request.POST)
                    if form.is_valid():
                        link = form.save()
    #                    link.save()
                        post.links.add(link)
                        args.update({'result': 'your link got added'})
                    else:
                        args.update({'result': 'your link did not validate...'})
            except:
                args.update({'result': 'not a link'})
    args.update({'post':post})
    args.update({'tag_form':TagForm()})
    args.update({'link_form':LinkForm()})
    args.update(csrf(request))
    return render_to_response('post/basic.html', args)

