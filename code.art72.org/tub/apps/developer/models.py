from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import admin
from django.dispatch import receiver 
from django.db.models.signals import post_save, pre_save
from django.utils.encoding import smart_str
import os
from uuid import uuid4
from sorl import thumbnail
import Image
from django.contrib.sites.models import Site
import simplejson
import urllib2 as urllib
from social_auth.models import UserSocialAuth
from apps.project.models import *
from test.test_imageop import MAX_LEN

MAX_IMAGE_SIZE = ('300','300')

class Developer(models.Model):
    """
    Extra user info that makes up an Developer.
    """
    #TODO: when checking for unique email, check for things like 'zackdever@gmail.com' vs 'zackdever+foo@gmail.com' and periods. not sure if this is specific to gmail or not
    # user data
    ALL_PROVIDERS = (('github','github'), ('google','google'),('twitter','twitter'), ('flickr','flickr'),('facebook','facebook'),('dropbox','dropbox',))
    
    user = models.OneToOneField(User)
    statement = models.TextField(null=True, blank=True)
    image = thumbnail.ImageField(upload_to='images/developers/%Y/%m/%d', null=True, blank=True)
    __original_image = None
    about = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    long = models.CharField(max_length=50, blank=True, null=True)
    process = models.TextField(blank=True, null=True)
    repos = models.ManyToManyField(Repo, default=None, null=True, blank=True)
    medias = models.ManyToManyField(Media, default=None, null=True, blank=True)
    projects = models.ManyToManyField(Project, default=None, null=True, blank=True)
    providers = models.CharField(choices=ALL_PROVIDERS, max_length=20, null=True, blank=True)
    # external id links
    
    def get_absolute_url(self): 
        current_site = Site.objects.get_current()
        return "http://%s/profile/%s" % (current_site.domain, self.user.username)
        
    def __unicode__(self):
        if self.user.get_full_name() != '':
            return self.user.get_full_name()
        else:
            return self.user.username 
    
    def rename_image_file(self):
        """
        Generate a UUID for the file name and 
        append the appropriate extension based off the format of the file.
        """
        img = Image.open(self.image)
        self.image.name = "%s.%s" % (uuid4(), img.format.lower())
    
    def do_resizes(self):
        """
        Only allow images to be MAX_IMAGE_SIZE.
        #TODO: check file size rather than max resolution
        """
        img = Image.open(self.image.path)
        img.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
        img.save(self.image.path)
        
    def videos(self):
        videos = {}
        for handle in self.externalid_set.filter(type=6):#vimeo
            url = 'http://vimeo.com/api/v2/user/%s/videos.json' % handle.handle
            file = urllib2.urlopen(url)
            content = file.read()     
            json = simplejson.loads(content)
            for video in json:
                url = "http://player.vimeo.com/video/%s" % video['url'].strip('http://vimeo.com') 
                videos.update({url: url})
#        for handle in self.externalid_set.filter(type=7):#youtube
#            url = 'https://gdata.youtube.com/feeds/api/users/%s/uploads?alt=json' % handle.handle
#            file = urllib2.urlopen(url)
#            content = file.read()     
#            json = simplejson.loads(content)
#            for video in json:
#                videos.update({video['entry']: video['entry']})
        print videos
        return videos
    
    def update_repos(self):
        github = self.user.social_auth.filter(provider='github')[0]
        repos = urllib.urlopen('https://api.github.com/users/%s/repos' % github.user)
        repos = simplejson.loads(repos.read())
        names = {}
        c = 0
        for repo in repos:
            rep = Repo.objects.get_or_create(title=repo['name'])[0]
            rep.blurb = repo['description']
            rep.url = repo['html_url']
            dev = repo['owner']
            dev = dev['login']
            rep.save() 
            self.repos.add(rep)
            print repo['name']
        return Repo.objects.all()
     
    def update_media(self):
        print 'updating the medias'
        youtube = self.user.social_auth.filter(provider='google')[0]
        medias = urllib.urlopen('https://gdata.youtube.com/feeds/api/videos?author=%s&alt=json&prettyprint=true' % youtube.user)
        medias = simplejson.loads(medias.read())
        names = {}
        c = 0
        medias = medias['feed']
        medias = medias['entry']
        for media in medias:
            tmp = media['title']
            tmp = tmp['$t']
            med = Media.objects.get_or_create(title=tmp)[0]
#            tmp = media['media$thumbnail'] # for image at some point
#            tmp = tmp['$t']
#            med.image
            tmp = media['media$group']
            tmp = tmp['media$content']
            tmp = tmp[0]
            tmp = tmp['url'] 
            print tmp
            med.video = tmp
            med.developer = tmp
            med.save() 
            self.medias.add(med)
        return Media.objects.all()
        
        
    def save(self, *args, **kwargs):
        image_changed = self.image != self.__original_image
        if image_changed:
            self.rename_image_file()
            self.__original_image = self.image
        if self.user.is_staff:
            super(Developer, self).save(*args, **kwargs)
        if image_changed and self.image:
            self.do_resizes() 

ID_TYPES = (
            ('1', 'github'),
            ('2', 'bitbucket'),
            ('3', 'source_forge'),
            ('4', 'stack_overflow'),
            ('5', 'twitter'),
            ('6', 'vimeo'),
            ('7', 'youtube')
    )
@receiver(post_save, sender=User, weak=False)
def delete_image_on_file(sender, instance, raw, created, using, **kwargs):
    if created:
        Developer.objects.create(user=instance)
        
@receiver(pre_save, sender=User, weak=False)
def ensure_unique_email(sender, instance, raw, using, **kwargs):
    users = User.objects.filter(email__iexact=instance.email)
    if users and users[0].id != instance.id:
        raise ValidationError("The email '%s' is already associated with another account." % instance.email)
    users = User.objects.filter(username__iexact=instance.username)
    if users and users[0].id != instance.id:
        raise ValidationError("The username '%s' is already associated with another account." % instance.username)