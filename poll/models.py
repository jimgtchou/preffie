from django.db import models
from django.conf import settings
from social_django.models import UserSocialAuth

import time
from uuid import uuid4
import os.path

def path_and_rename(instance,filename, option):
    upload_to = 'media'
    ext = filename.split('.')[-1]
    filename = '{}_{}.{}'.format(uuid4().hex, option, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_a(instance,filename):
    return path_and_rename(instance,filename, 'a')

def path_and_rename_b(instance,filename):
    return path_and_rename(instance,filename, 'b')

# Create your models here.
class Poll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='poll_created')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    media_type = models.CharField(max_length=10, default='image', blank=True)
    poll_media_count = models.IntegerField(default=2, blank=True)
    link = models.URLField(blank=True)
    media_a = models.FileField()
    media_b = models.FileField()
    # TODO: django-imagekit
    vote_a_count = models.IntegerField(default=0, blank=True)
    vote_b_count = models.IntegerField(default=0, blank=True)
    caption = models.CharField(max_length=2200, blank=True)
    # TODO: tags

    def __str__(self):
        return '{}_{}'.format(self.user.username, self.id)

    def get_absolute_url(self):
        return reverse('poll:detail', args=[self.id])

    def get_api_vote_url_a(self):
        return reverse("poll:vote-api", kwargs={"id": self.id, "choice":"a"})

    def get_api_vote_url_b(self):
        return reverse("poll:vote-api", kwargs={"id": self.id, "choice":"b"})

class Vote(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='voted_on')
    poll =  models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='voted_for')
    OPTION = (('a', 'mediaA'), ('b', 'mediaB'))
    choice = models.CharField(max_length=10, choices=OPTION)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
