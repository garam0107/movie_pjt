from rest_framework import serializers
from .models import Genre,Movie,Actor,Movie_review,MovieReview_comment



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields= '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields= '__all__'

class MoiveSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only = True, many = True)
    actors = ActorSerializer(read_only =True, many = True)
    class Meta:
        model = Movie
        fields = '__all__'


class MovieReviewsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  
    class Meta:
        model = Movie_review
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'likes_count', 'rating', 'username']

class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview_comment
        fields = ['content']
        read_only_fields = ['review','reviewuser']