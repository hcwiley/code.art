from django.conf import settings
from django.contrib import admin
from django.db import models
from uuid import uuid4
from sorl import thumbnail
import Image
from django.template.defaultfilters import slugify
import urllib
import json as simplejson
#from apps.developer.models import *
from apps.utility.models import Tag, Link

MAX_IMAGE_SIZE = settings.MAX_IMAGE_SIZE

class Repo(models.Model):
    title = models.CharField(max_length=144)
    blurb = models.TextField(default="", null=True, blank=True)
    url = models.URLField()
    dependencies = models.ManyToManyField(Link, null=True, blank=True, default=None)
    tags = models.ManyToManyField(Tag, null=True, blank=True, default=None)
    
    def __unicode__(self):
        return self.title
    
    def get_commits(self):
        if self.developer_set.count() > 0:
            github = self.developer_set.all()[0]
            github = github.user.social_auth.filter(provider='github')[0]
            print 'https://api.github.com/repos/%s/%s/commits?client_id=%s&client_secret=%s' % (github.user, self.title, settings.GITHUB_APP_ID, settings.GITHUB_API_SECRET)
            commits = urllib.urlopen('https://api.github.com/repos/%s/%s/commits?client_id=%s&client_secret=%s' % (github.user, self.title, settings.GITHUB_APP_ID, settings.GITHUB_API_SECRET))
            commits = simplejson.load(commits)
            return commits
        else:
            return None
    
    def getBlurb(self, developer):
        github = developer.user.social_auth.filter(provider='github')[0]
        repos = urllib.urlopen('https://api.github.com/repos/%s/%s' % (github.user, self.title))
        repos = simplejson.loads(repos.read())
        print 'des: %s' % repos['description']
        return repos['description']
    
    def get_dates_rivisions(self):
        return "foo"

class ExtendedImage(models.Model):
    uploaded = thumbnail.ImageField(upload_to='images/projects/%Y/%m/%d', null=True, blank=True, default=None)
    external = models.URLField(null=True, blank=True, default="")
    
    def __unicode__(self):
        if self.uploaded:
            return self.uploaded
        elif self.external:
            return self.external

    def url(self):
        if self.external:
            return self.external
        elif self.uploaded:
            return self.uploaded
        else:
            return ""


class Media(models.Model):
    title = models.CharField(max_length=144)
    image = models.ForeignKey(ExtendedImage, null=True, blank=True, default=None)
    video = models.URLField(max_length=400, null=True, blank=True, default=None)
    date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']
    
    def get_image(self):
        return self.image.url()


class Project(models.Model):
    title = models.CharField(max_length=144)
    slug = models.SlugField(editable=False, default="")
    blurb = models.TextField(default="", null=True,blank=True)
    use_git_blurb = models.BooleanField(default=False)
    repos = models.ManyToManyField(Repo, null=True,blank=True)
    media = models.ManyToManyField(Media, null=True,blank=True)
#    date = models.ForeignKey(Date, null=True, blank=True)
    image = models.ForeignKey(ExtendedImage, null=True, blank=True)
    __original_image = None
    
    @models.permalink
    def get_absolute_url(self):
        return ('apps.project.views.project', {self.id:self.id})
    
    def __unicode__(self):
        return self.title
    
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
        
    def getGithubBlurb(self, repo):
        return repo.getBlurb(self.developer_set.all()[0])

    def get_image(self):
        if self.image:
            return self.image.url()
        elif self.media.count() > 0:
            return self.media.all()[0].get_image()
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        try:
            if self.use_git_blurb:
                if self.repos.count() > 0:
                    self.blurb = self.getGithubBlurb(self.repos.all()[0])
                    self.repos.all()[0].blurd = self.blurb
        except:
            print 'oh well'
        if Project.objects.filter(title=self.title).count() > 1:
            return 'there is already a post with that name'
        if self.image:
            image_changed = self.image != self.__original_image
            if image_changed:
                self.rename_image_file()
                self.__original_image = self.image
        super(Project, self).save(*args, **kwargs) 
        print self.blurb
        if self.image and image_changed:
            self.do_resizes()
