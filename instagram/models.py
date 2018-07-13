from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    profile_picture = models.FileField(upload_to="media/")
    status = models.CharField(max_length=1024)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Followers(models.Model):
    follower_id = models.IntegerField()
    following_id = models.IntegerField()

class Posts(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.FileField(default = "182.jpg", upload_to="media/")
    time_stamp = models.DateTimeField(auto_now_add=True, editable = False, null = False, blank = False)
    likes = models.ManyToManyField(User, blank=True)