from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from apps.oauth2_lite_client import oauth2_client

class Provider(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    authorization_url = models.URLField()
    token_url = models.URLField()
    redirect_url = models.URLField()
    scope = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_authorization_url(self):
        client = oauth2_client.Client(self.client_id, self.client_secret)
        return client.authorization_url(self.authorization_url, self.redirect_url, self.scope)

    def save(self):
        slug = "%s" % slugify(self.name)
        self.slug = slug
        super(Provider, self).save()

    def __unicode__(self):
        return '%s' % self.name
    class Admin:
        pass

class Credential(models.Model):
    user = models.ForeignKey(User)
    provider = models.ForeignKey(Provider)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return '%s at %s' % (self.user, self.provider)
    class Admin:
        pass
