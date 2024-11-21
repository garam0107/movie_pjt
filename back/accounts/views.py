from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render,get_list_or_404,get_object_or_404

from dj_rest_auth.models import TokenModel
from dj_rest_auth.app_settings import api_settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from diaries.models import Diary
from movies.models import Movie_review
from .serializers import UserFollowingDiarySerializer,UserFollowingReviewSerializer,UserSerializer,UserUpdateSerializer
# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = api_settings.REGISTER_SERIALIZER
    permission_classes = api_settings.REGISTER_PERMISSION_CLASSES
    token_model = TokenModel
    throttle_scope = 'dj_rest_auth'

@api_view(['GET','POST','DELETE','PUT'])
@permission_classes([IsAuthenticated])
def mypage(request, user_username):
    User = get_user_model()
    user = get_object_or_404(User, username = user_username)
    if request.method == 'GET':
        user.visit_count += 0.5
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    # elif request.method == 'POST':
    #     pass
    # elif request.method == 'POST':
    #     pass
    # elif request.method == 'POST':
    #     pass




@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def follow(request, user_username):
    User = get_user_model()
    target_user = get_object_or_404(User, username = user_username)
    if request.method =='POST':
        if request.user == target_user:
            return JsonResponse({'error' :'자기 자신을 팔로우할 수 없습니다.'}, status = status.HTTP_400_BAD_REQUEST)
       
        if target_user in request.user.followings.all():
            request.user.followings.remove(target_user)
            is_following = False
            return JsonResponse({'message': '언팔로우',
                                 'is_following': is_following})
        else:
            request.user.followings.add(target_user)
            is_following = True
            return JsonResponse({'message': '팔로우',
                                 'is_following' : is_following})
    elif request.method == 'GET':
        user = request.user
        following_users = user.followings.all()

        diaries = Diary.objects.filter(author__in = following_users)
        reviews = Movie_review.objects.filter(user__in = following_users)

        serializer_diaries = UserFollowingDiarySerializer(diaries, many = True)
        serializer_reviews = UserFollowingReviewSerializer(reviews, many = True)
        return Response({
            'diaries' : serializer_diaries.data,
            'review' : serializer_reviews.data
        })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request, user_username):
    User = get_user_model()
    user = get_object_or_404(User, username = user_username)
    serializer = UserUpdateSerializer(user, data = request.data, partial = True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

