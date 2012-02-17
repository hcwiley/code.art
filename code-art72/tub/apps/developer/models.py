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

MAX_IMAGE_SIZE = ('300','300')

class Developer(models.Model):
    """
    Extra user info that makes up an Developer.
    """
    #TODO: when checking for unique email, check for things like 'zackdever@gmail.com' vs 'zackdever+foo@gmail.com' and periods. not sure if this is specific to gmail or not
    # user data
    user = models.OneToOneField(User)
    statement = models.TextField(null=True, blank=True)
    image = thumbnail.ImageField(upload_to='images/developers/%Y/%m/%d', null=True, blank=True)
    __original_image = None
    about = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    long = models.CharField(max_length=50, blank=True, null=True)
    # external id links
    github_id = models.CharField(max_length=50, blank=True, null=True)
    bitbucket_id = models.CharField(max_length=50, blank=True, null=True)
    stack_over_id = models.CharField(max_length=50, blank=True, null=True)
    source_forge_id = models.CharField(max_length=50, blank=True, null=True)
    twitter_id = models.CharField(max_length=50, blank=True, null=True) 
    vimeo_id = models.CharField(max_length=50, blank=True, null=True)
    youtube_id = models.CharField(max_length=50, blank=True, null=True)
    
    def get_absolute_url(self): 
        current_site = Site.objects.get_current()
        return "http://%s/%s" % (current_site.domain, self.user.username)
        
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
        
    def save(self, *args, **kwargs):
        image_changed = self.image != self.__original_image
        if image_changed:
            self.rename_image_file()
            self.__original_image = self.image
        super(Developer, self).save(*args, **kwargs)
        if image_changed:
            self.do_resizes() 
        
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
