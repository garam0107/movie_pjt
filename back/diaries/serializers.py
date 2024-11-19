from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Diary
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