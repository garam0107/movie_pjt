from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model,logout
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
from .serializers import UserFollowingDiarySerializer,UserFollowingReviewSerializer,UserSerializer,UserUpdateSerializer,AllUserSerializer
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
    if user != request.user:
        user.visit_count += 0.5
        user.save()
    if request.method == 'GET':
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
        is_following = target_user in request.user.followings.all()
        diaries = Diary.objects.filter(author__in = following_users)
        reviews = Movie_review.objects.filter(user__in = following_users)

        serializer_diaries = UserFollowingDiarySerializer(diaries, many = True)
        serializer_reviews = UserFollowingReviewSerializer(reviews, many = True)
        return Response({
            'diaries' : serializer_diaries.data,
            'review' : serializer_reviews.data,
            'is_following': is_following
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

@api_view(['GET'])
def top_users_by_stone(request):
    User = get_user_model()
    top_users = User.objects.all().order_by('-stone')[:4]
    serializer = AllUserSerializer(top_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def check_username(request):
    username = request.query_params.get('username', None)
    if username:
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return Response({'available' : False, 'message': '이미 사용 중인 ID입니다.'})
        return Response({'available' : True, 'message': '사용 가능한 ID입니다.'})
    return Response({'error': 'username 파라미터가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request):
    user = request.user
    password = request.data.get('password')

    if not password:
        return Response({'message' : '비밀번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.check_password(password):
        return Response({'message': '비밀번호가 틀렸습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.delete()
    logout(request)
    return Response({'message' : '회원 탈퇴'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def public(request,user_username):
    now_user = get_user_model()
    target_user = get_object_or_404(now_user, username = user_username)
    user = request.user
    if user == target_user:
        user.is_public = not user.is_public
        user.save()

    # 성공적으로 저장된 경우 응답 반환
    return Response({
        "message": "공개 상태가 성공적으로 변경되었습니다.",
        "is_public": user.is_public
    }, status=200)

   
