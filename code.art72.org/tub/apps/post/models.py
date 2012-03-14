from django.conf import settings
from django.contrib import admin
from apps.developer import *
from django.db import models
from uuid import uuid4
from sorl import thumbnail
import Image
from apps.developer.models import *
from django.db import models
import urllib
#import BeautifulSoup

MAX_IMAGE_SIZE = settings.MAX_IMAGE_SIZE

class Post(models.Model):
    title = models.CharField(max_length=144)
    blurb = models.TextField()
#    developer = models.ForeignKey(Developer)
    image = thumbnail.ImageField(upload_to='images/posts/%Y/%m/%d', null=True, blank=True)
    __original_image = None
    
    @models.permalink
    def get_absolute_url(self):
        return ('apps.post.views.post', {self.id:self.id})
    
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
        if Post.objects.filter(title=self.title).count() > 0:
            return 'there is already a post with that name'
        image_changed = self.image != self.__original_image
        if image_changed:
            self.rename_image_file()
            self.__original_image = self.image
        super(Post, self).save(*args, **kwargs)
        if image_changed:
            self.do_resizes()

class Link(models.Model):
    url = models.URLField(help_text='add your own link here')
    post = models.ForeignKey(Post)
    title = models.CharField(max_length=100, null=False, blank=True)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
#        if self.title == '':
#            soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(self.url))
#            self.title = soup.title.string
        super(Link, self).save(*args, **kwargs)
    

class Tag(models.Model):
    text = models.CharField(max_length=50, help_text='add your own tag here')
    post = models.ManyToManyField(Post)
    
    def __unicode__(self):
        return self.text
    
    @models.permalink
    def get_absolute_url(self):
        return ('apps.post.views.tag', {self.id:self.id})
