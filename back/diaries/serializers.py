from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Diary
from movies.models import Movie

user = get_user_model()

class DiaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['gpt_comment','title','content']



class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'