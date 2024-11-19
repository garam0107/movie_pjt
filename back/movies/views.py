from django.http import JsonResponse
from django.shortcuts import render,get_list_or_404,get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from .models import Genre,Actor,Movie,Movie_review
from .serializers import GenreSerializer,ActorSerializer,MoiveSerializer,MovieReviewsSerializer
# Create your views here.
@api_view(['GET'])
def main(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MoiveSerializer(movies, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk = movie_pk)
        serializer = MoiveSerializer(movie)
        return Response(serializer.data)
    
@api_view(['POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def create_review(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    rating = request.data.get('rating')

    if not rating:
        return Response({'message' : '별점을 선택해주세요.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = MovieReviewsSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = user , movie = movie)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == "PUT":
        review = Movie_review.objects.filter(movie = movie, user = user).first()
        if not review:

            return Response({'message' : '리뷰가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieReviewsSerializer(review, data = request.data, partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    elif request.method == 'DELETE':
        review = Movie_review.objects.filter(movie = movie, user = user).first()
        if not review:   
            return Response({'message' : '리뷰가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({'message' : '리뷰가 삭제되었습니다.'}, status= status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    if request.method == 'POST':
        user = request.user
        movie = get_object_or_404(Movie, pk = movie_pk)
        if user in movie.like_users.all():
            movie.like_users.remove(user)
            liked = False
        else:
            movie.like_users.add(user)
            liked = True
        like_count = movie.like_users.count()

        return JsonResponse({
            'liked' : liked,
            'like_count' : like_count
        })
@api_view(['GET'])
def detail_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    serializer = MovieReviewsSerializer(movie, many = True)
    return Response(serializer.data)
