from django.conf import settings
from django.contrib import admin
from django.db import models
from uuid import uuid4
from sorl import thumbnail
import Image
from apps.developer.models import Developer
from apps.utility.models import *
#import BeautifulSoup

MAX_IMAGE_SIZE = settings.MAX_IMAGE_SIZE

class Post(models.Model):
    title = models.CharField(max_length=144)
    blurb = models.TextField()
    image = thumbnail.ImageField(upload_to='images/posts/%Y/%m/%d', null=True, blank=True)
    links = models.ManyToManyField(Link, null=True, blank=True, default=None)
    developer = models.ForeignKey(Developer, default='Mr. Bar', null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True, default=None)
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
\