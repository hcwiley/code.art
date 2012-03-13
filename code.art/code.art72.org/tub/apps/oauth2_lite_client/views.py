import urlparse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from models import Provider, Credential
from apps.developer.views import *
from apps.oauth2_lite_client import oauth2_client
from django.contrib.auth.models import AnonymousUser

def get_all_repos(request):
    user = request.user
    github = Provider.objects.get(slug='github')
#    cred = user.credential_set.get(provider=github)
    return None
#    if github:
#        client = oauth2_client.Client(github.client_id, github.client_secret)
#        return client.request("https://api.github.com/user/repos", None, None)

def provider_cb(request, slug = None):
    print "slug: %s" % slug
    providers = Provider.objects.all()
#    print request.user.username
#    if request.user.username == "":
#        return redirect('/login')
#    else:
#    my_providers = Credential.objects.filter(user = request.user)
    if len(slug) > 0:
        provider = Provider.objects.get(slug = slug)
        credential, created = Credential.objects.get_or_create(provider = provider)
        code = request.GET.get('code', None)
        if code:
            print "code: %s" % code
            print "provider %s" % provider
            client = oauth2_client.Client(provider.client_id, provider.client_secret)
            access_token, refresh_token = client.redeem_code(refresh_uri = provider.token_url, redirect_uri = provider.redirect_url, code = code, provider = provider)
            print "access_token: %s" % access_token
            print "refresh_token: %s" % refresh_token 
            if access_token and refresh_token:
                credential.access_token = access_token
                credential.refresh_token = refresh_token
                credential.save()
                return HttpResponseRedirect(".")
        if not credential.access_token:
            return HttpResponseRedirect(provider.get_authorization_url())
    return render_to_response('oauth2_lite_client/oauth2_lite_client.html',
                                                                {
                                                                'providers': providers,
#                                                                'my_providers': my_providers,
                                                                'repos' : get_all_repos(request)
                                                                }, RequestContext(request))
