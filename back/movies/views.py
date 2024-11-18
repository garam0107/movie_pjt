from django.shortcuts import render,get_list_or_404,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GenreSerializer,ActorSerializer,MoiveSerializer
from .models import Genre,Actor,Movie
# Create your views here.
@api_view(['GET'])
def main(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MoiveSerializer(movies, many = True)
        return Response(serializer.data)

@api_view(['GET','POST','PUT','DELETE'])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk = movie_pk)
        serializer = MoiveSerializer(movie)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
@api_view(['POST'])
def movie_like(request, movie_pk):
    pass

@api_view(['GET'])
def detail_review(request):
    pass