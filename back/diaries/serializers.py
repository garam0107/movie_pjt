from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Diary,Diary_comment
from movies.models import Movie

user = get_user_model()


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'
        read_only_fields = ['author']

class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['date', 'mood_emoji','title', 'content']
        read_only_fields = ['author']

class DiaryCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  
    class Meta:
        model = Diary_comment
        fields = ['username', 'content', 'created_at', 'user', 'diary']
        read_only_fields = ['user', 'diary']