from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class Actor(models.Model):
    name = models.CharField(max_length=50)
    poster_path = models.CharField(max_length=200, blank= True, null= True)

class Genre(models.Model):
    name = models.CharField(max_length=50) 

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(blank=True)  
    popularity = models.FloatField()
    vote_count = models.IntegerField()  
    vote_average = models.FloatField()  
    overview = models.TextField()
    runtime = models.IntegerField() 
    production_country = models.CharField(max_length=100)  
    poster_path = models.CharField(max_length=200, blank=True)   #이미지
    backdrop_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, blank=True)
    youtube_key = models.CharField(max_length=100, blank=True)
    actors = models.ManyToManyField(Actor, blank= True)
    director = models.CharField(max_length=100, blank=True)
    words = models.CharField(max_length=255, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)


class Movie_review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(null= True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_reviews')   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie', 'user'], name='unique_movie_user_review')
        ]


class MovieReview_comment(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Movie_review, on_delete=models.CASCADE)
    reviewuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['review', 'reviewuser'], name='unique_review_user_comment')
        ]

