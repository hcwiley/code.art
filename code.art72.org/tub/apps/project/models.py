from django.conf import settings
from django.contrib import admin
from apps.developer import *
from django.db import models
from uuid import uuid4
from sorl import thumbnail
import Image
from apps.developer.models import *
from django.template.defaultfilters import slugify
import urllib
import BeautifulSoup
from apps.post.models import *

MAX_IMAGE_SIZE = settings.MAX_IMAGE_SIZE

class Repo(models.Model):
    title = models.CharField(max_length=144)
    blurb = models.TextField(default="", null=True, blank=True)
    url = models.URLField()
    
    def __unicode__(self):
        return self.title

class ExtendedImage(models.Model):
    uploaded = thumbnail.ImageField(upload_to='images/projects/%Y/%m/%d', null=True, blank=True, default=None)
    external = models.URLField(null=True, blank=True, default="")
    
    def __unicode__(self):
        if self.uploaded:
            return self.uploaded
        elif self.external:
            return self.external


class Media(models.Model):
    title = models.CharField(max_length=144)
    image = models.ForeignKey(ExtendedImage, null=True, blank=True, default=None)
    video = models.URLField(null=True, blank=True, default=None)
    
    def __unicode__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=144)
    slug = models.SlugField(editable=False, default="")
    blurb = models.TextField()
    use_git_blurb = models.BooleanField(default=False)
    developer = models.ManyToManyField(Developer)
    repos = models.ManyToManyField(Repo, null=True,blank=False)
    media = models.ManyToManyField(Media, null=True,blank=False)
#    date = models.ForeignKey(Date, null=True, blank=True)
    image = thumbnail.ImageField(upload_to='images/projects/%Y/%m/%d', null=True, blank=True)
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
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if Post.objects.filter(title=self.title).count() > 0:
            return 'there is already a post with that name'
        image_changed = self.image != self.__original_image
        if image_changed:
            self.rename_image_file()
            self.__original_image = self.image
        super(Project, self).save(*args, **kwargs)
        if image_changed:
            self.do_resizes()
