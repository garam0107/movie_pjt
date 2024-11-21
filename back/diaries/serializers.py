from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Diary,Diary_comment
from movies.models import Movie

user = get_user_model()

# 일기 
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'
        read_only_fields = ['author']
# 일기 작성
class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['date', 'mood_emoji','title', 'content']
        read_only_fields = ['author']
# 일기의 댓글 작성
class DiaryCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  
    class Meta:
        model = Diary_comment
        fields = ['username', 'content', 'created_at', 'user', 'diary']
        read_only_fields = ['user', 'diary']


# 다이어리 상세 정보 조회
class DiaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'