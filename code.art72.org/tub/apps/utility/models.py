from django.conf import settings
from django.contrib import admin
from django.db import models
import urllib

class Tag(models.Model):
    text = models.CharField(max_length=50, help_text='add your own tag here', unique=True)
    
    def __unicode__(self):
        return self.text
    
    @models.permalink
    def get_absolute_url(self):
        return ('apps.post.views.tag', {self.id:self.id})


class Link(models.Model):
    url = models.URLField(help_text='add your own link here', unique=True)
    title = models.CharField(max_length=100, null=False, blank=True)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
#        if self.title == '':
#            soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(self.url))
#            self.title = soup.title.string
        super(Link, self).save(*args, **kwargs)
