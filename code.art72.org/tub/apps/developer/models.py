from django.db import models
from django.conf import settings
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
import json as simplejson
import urllib2 as urllib
from social_auth.models import UserSocialAuth
from apps.project.models import Project, Repo, Media, ExtendedImage
#from apps.post.models import Post
from datetime import datetime
from django.template.defaultfilters import slugify

MAX_IMAGE_SIZE = ('300', '300')

class Developer(models.Model):
    """
    Extra user info that makes up an Developer.
    """
    #TODO: when checking for unique email, check for things like 'zackdever@gmail.com' vs 'zackdever+foo@gmail.com' and periods. not sure if this is specific to gmail or not
    # user data
    ALL_PROVIDERS = (('github', 'github'), ('google', 'google'), ('twitter', 'twitter'), ('flickr', 'flickr'), ('facebook', 'facebook'), ('dropbox', 'dropbox',))
    
    user = models.OneToOneField(User)
    statement = models.TextField(null=True, blank=True)
    image = models.ForeignKey(ExtendedImage, null=True, blank=True)
    __original_image = None
    about = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    long = models.CharField(max_length=50, blank=True, null=True)
    process = models.TextField(blank=True, null=True)
#    posts = models.ManyToOneRel(Post)
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
            file = urllib.urlopen(url)
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
            self.save()
            try:
                proj = Project.objects.get(slug=rep.title) 
                if proj:
                    proj.repos.add(rep)
            except:
                print 'no auto project add'
            print repo['name']
        return self.repos.all()
    
    def updateYoutube(self):
        youtube = self.user.social_auth.filter(provider='google')[0]
        medias = urllib.urlopen('https://gdata.youtube.com/feeds/api/videos?author=%s&alt=json' % youtube.user)
        medias = simplejson.loads(medias.read())
        names = {}
        c = 0
        medias = medias['feed']
        try:
          medias['entry']
        except:
          return
        medias = medias['entry']
        for media in medias:
            tmp = media['title']
            tmp = tmp['$t']
            med = Media.objects.get_or_create(title=tmp)[0]
            tmp = media['media$group']
            tmp = tmp['media$content']
            tmp = tmp[0]
            tmp = tmp['url'] 
            med.video = tmp
            med.developer = tmp
            tmp = media['media$group']
            tmp = tmp['media$thumbnail']
            tmp = tmp[0]
            tmp = tmp['url']
            med.image = ExtendedImage.objects.get_or_create(external=tmp)[0]
            tmp = media['published']
            tmp = tmp['$t']
            tmp = datetime.strptime(tmp, '%Y-%m-%dT%H:%M:%S.000Z')
            med.date = tmp
            med.save()
            #Auto project tagging 
            try:
                tmp = media['media$group']
                tmp = tmp['media$description']
                tmp = tmp['$t']
                at = tmp.find('@')
                if at >= 0:
                    tmp = tmp[at+1:]
                    #print tmp
                    tmp = tmp.split(' ')[0]
                    #print tmp
                    proj = Project.objects.get(slug=tmp)
                    if proj:
                        print 'project: %s' % proj
                        proj.media.add(med)
            except:
                print 'no go on the auto add'
            self.medias.add(med)
            self.save()
#        print 'updated from youtube'
            
    def updatePicasa(self):
        picasa = self.user.social_auth.filter(provider='google')[0]
        albums = urllib.urlopen('https://picasaweb.google.com/data/feed/api/user/%s?alt=json' % picasa.user)
        albums = simplejson.loads(albums.read())
        names = {}
        c = 0
        albums = albums['feed']
        albums = albums['entry']
        print 'bout to get all the albums'
        print len(albums)
        for album in albums:
            try:
                tmp = album['link'][0]
                tmp = tmp['href']
                medias = urllib.urlopen('%s' % tmp)
                medias = simplejson.loads(medias.read())
                medias = medias['feed']
                medias = medias['entry']
                for media in medias:
                    tmp = media['title']
                    tmp = tmp['$t']
                    med = Media.objects.get_or_create(title=tmp)[0]
                    #image
                    tmp = media['media$group']
                    tmp = tmp['media$content']
                    tmp = tmp[0]
                    tmp = tmp['url']
                    med.image = ExtendedImage.objects.get_or_create(external=tmp)[0]
                    #date
                    tmp = media['published']
                    tmp = tmp['$t']
                    tmp = datetime.strptime(tmp, '%Y-%m-%dT%H:%M:%S.000Z')
                    med.date = tmp
                    #video?
                    tmp = media['media$group']
                    tmp = tmp['media$content']
                    if len(tmp) > 1:
                        tmp = tmp[2]
                        tmp = tmp['url'] 
    #                print tmp
                        med.video = tmp
                    med.developer = tmp
                    med.save()
                    self.medias.add(med)
                    self.save()
            except:
                print 'err.. there was an api error'
#        print "updated from picasa"

    def updateDropbox(self):
        dropbox = self.user.social_auth.filter(provider='dropbox')[0]
        #albums = urllib.urlopen('https://www.dropbox.com/1/oauth2/authorize')
        albums = urllib.urlopen('https://api.dropbox.com/1/search/.jpg?token=2g3j61j07bybzfh4')
        albums = simplejson.loads(albums.read())
        print albums
     
    def update_media(self):
        self.updateYoutube()
        self.updatePicasa()
        #self.updateDropbox()
        return self.medias.all()
        
        
    def save(self, *args, **kwargs):
        if len(self.user.social_auth.filter(provider='github')) > 0:
            github = self.user.social_auth.filter(provider='github')[0]
            repos = urllib.urlopen('https://api.github.com/users/%s?client_id=%s&client_secret=%s' % (github.user, settings.GITHUB_APP_ID, settings.GITHUB_API_SECRET))
            repos = simplejson.loads(repos.read())
#            print repos
            self.image = ExtendedImage.objects.get_or_create(external=repos['avatar_url'])[0]
            self.image.save()
        super(Developer, self).save(*args, **kwargs)

ID_TYPES = (
            ('1', 'github'),
            ('2', 'bitbucket'),
            ('3', 'source_forge'),
            ('4', 'stack_overflow'),
            ('5', 'twitter'),
            ('6', 'vimeo'),
            ('7', 'youtube')
    )
        
@receiver(pre_save, sender=User, weak=False)
def ensure_unique_email(sender, instance, created=False, raw=False, using=False, update_fields=False, **kwargs):
  print "pre user save"
  print instance
    #users = User.objects.filter(email=instance.email)
    #if users and users[0].id != instance.id:
        #print "email error"
        #raise ValidationError("The email '%s' is already associated with another account." % instance.email)
    #users = User.objects.filter(username__iexact=instance.username)
    #if users and users[0].id != instance.id:
        #print "username error"
        #raise ValidationError("The username '%s' is already associated with another account." % instance.username)
