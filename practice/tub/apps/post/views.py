from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from django.core.context_processors import csrf
from tub.views import common_args
from apps.post.forms import *

def list_post(request):
    args.update({'post_form':PostForm(instance=post)})
    args.update(csrf(request))
    return render_to_response('post/list.html', args)

def post(request, id):
    args = common_args(request)
    if id == '':
        return redirect('list_posts')
    post = Post.objects.get(id=id)
    if request.POST:
        if request.POST['text']:
            try:
                print 'text'
                form = TagForm(request.POST, instance=post)
                if form.is_valid():
                    print 'valid'
                    tag.post += post
                    if form.save(commit=False):
                          pass
                    else:
                        print 'no save'
                    print tag.post
                    tag.save()
                    args.update({'result': 'your tag got added'})
                else:
                    args.update({'result': 'your tag did not validate...'})
            except:
                args.update({'result': 'that was bad...'})
        elif request.POST['url']:
            try:
                print 'url'
                form = LinkForm(request.POST, instance=post)
                if form.is_valid():
                    link = form.save(commit=False)
                    link.post = post
                    link.save()
                    args.update({'result': 'your link got added'})
                else:
                    args.update({'result': 'your link did not validate...'})
            except:
                    args.update({'result': 'ummmm whoops...'})
    args.update({'post':post})
    args.update({'tag_form':TagForm(instance=post)})
    args.update({'link_form':LinkForm(instance=post)})
    args.update(csrf(request))
    return render_to_response('post/basic.html', args)

def tag(request, id):
    args = common_args(request)
    tag = Tag.objects.get(id=id)
    posts = tag.post.all()
    args.update({'posts': posts})
    args.update(csrf(request))
    return render_to_response('tag.html', args)
