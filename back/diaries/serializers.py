from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Diary


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['date', 'mood_emoji']