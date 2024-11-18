from django.db import models
from movies.models import Movie
from django.conf import settings
# Create your models here.

class Diary(models.Model):
    date = models.DateField(auto_now_add=True)
    mood_emoji = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    gpt_comment = models.TextField()
    recommend_movie = models.ManyToManyField(Movie, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_diaries', blank=True)

class Diary_comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)

