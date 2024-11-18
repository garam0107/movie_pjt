from rest_framework import serializers
from .models import Genre,Movie,Actor



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