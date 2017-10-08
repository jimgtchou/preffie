from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    userid = models.FloatField(unique=True)
    username = models.CharField(max_length=30)
    profile_picture_url = models.URLField(blank=True)
    full_name = models.CharField(max_length=30)
    bio = models.CharField(max_length=150)
    website = models.URLField(blank=True)
    is_business = models.BooleanField(default=False)
    media_count = models.IntegerField(default=0)
    follows_count = models.IntegerField(default=0)
    folowed_by_count = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

class Follow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_relationship')
    follows =  models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_follows')
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
