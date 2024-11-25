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

# 영화 정보
class MoiveSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only = True, many = True)
    actors = ActorSerializer(read_only =True, many = True)
    class Meta:
        model = Movie
        fields = '__all__'

# 영화 리뷰
class MovieReviewsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    
    class Meta:
        model = Movie_review
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'likes_count', 'rating', 'username','nickname']

#영화 리뷰의 댓글
class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview_comment
        fields = ['content']
        read_only_fields = ['review','reviewuser']


class MovieSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title','id']