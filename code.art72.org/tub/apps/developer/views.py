from django.conf import settings
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from django.contrib.admin.models import User
from tub.views import common_args
from oauth2app.models import Client

Client.objects.create(
    name="OAuth 2.0 Client",
    user=user)

def profile(request, developer):
    args = common_args(request)
    args.update({'developer': Developer.objects.get(user=User.objects.get(username=developer))})
    args['base_template'] = 'developer/profile_base.html'
    return render_to_response('developer/profile.html', args)

def profile_redirect(request):
    return redirect("/profile/%s" % (request.user.username))

def edit_repos(request, developer):
    args = common_args(request)
    if args['developer'] == None:
        return redirect("/accounts/login")
    return render_to_response('developer/repos.html', args)

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from django import forms

class AuthorizeForm(forms.Form):
    pass

@login_required
def missing_redirect_uri(request):
    return render_to_response(
        'oauth2/missing_redirect_uri.html',
        {},
        RequestContext(request))

@login_required
def authorize(request):
    authorizer = Authorizer()
    try:
        authorizer.validate(request)
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    if request.method == 'GET':
        template = {}
        # Use any form, make sure it has CSRF protections.
        template["form"] = AuthorizeForm()
        # Appends the original OAuth2 parameters.
        template["form_action"] = '/oauth2/authorize?%s' % authorizer.query_string
        return render_to_response(
            'oauth2/authorize.html',
            template,
            RequestContext(request))
    elif request.method == 'POST':
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            if request.POST.get("connect") == "Yes":
                # User agrees. Redirect to redirect_uri with success params.
                return authorizer.grant_redirect()
            else:
                # User refuses. Redirect to redirect_uri with error params.
                return authorizer.error_redirect()
    return HttpResponseRedirect("/")

from oauth2app.authenticate import Authenticator, AuthenticationException
from django.http import HttpResponse

def test(request):
    authenticator = Authenticator()
    try:
        # Validate the request.
        authenticator.validate(request)
    except AuthenticationException:
        # Return an error response.
        return authenticator.error_response(content="You didn't authenticate.")
    username = authenticator.user.username
    return HttpResponse(content="Hi %s, You authenticated!" % username)