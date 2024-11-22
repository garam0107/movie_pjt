from django.db import models
from movies.models import Movie
from django.conf import settings
# Create your models here.

class Diary(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diaries')
    date = models.DateField(auto_now_add=True)
    mood_emoji = models.CharField(max_length=100, choices=[
        ('emotions/angry.jpg', '분노'),
        ('emotions/calm.jpg', '평온'),
        ('emotions/excited.jpg', '신남'),
        ('emotions/happy.jpg', '행복'),
        ('emotions/sad.jpg', '슬픔'),
        ('emotions/sleepy.jpg','지루'),
    ])
    title = models.CharField(max_length=100)
    content = models.TextField()
    gpt_comment = models.TextField(blank=True, null= True)
    recommend_movie = models.ManyToManyField(Movie, blank=True)
    recommend_movie_titles = models.JSONField(blank=True, null=True)
    recommend_reasons = models.JSONField(blank=True, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_diaries', blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'date'], name='unique_author_daily_diary')
        ]
class Diary_comment(models.Model):
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='comments')

