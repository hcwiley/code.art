from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from django.contrib.admin.models import User
from tub.views import common_args


def profile(request, developer):
    args = common_args(request)
    args.update({'developer': Developer.objects.get(user=User.objects.get(username=developer))})
    args['base_template'] = 'developer/profile_base.html'
    return render_to_response('developer/profile.html', args)

def profile_redirect(request):
    return redirect("/profile/%s" % (request.user.username))

def edit_repos(request, developer):
    args = common_args(request)
    repos = request.user.developer.update_repos()
    args['repos'] = repos
    if args['developer'] == None:
        return redirect("/accounts/login")
    return render_to_response('developer/repos.html', args)