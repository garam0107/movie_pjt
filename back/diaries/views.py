import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, get_list_or_404, get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from .models import Diary
from .serializers import DiaryCreateSerializer, DiarySerializer,DiaryCommentSerializer
# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_diary(request, user_pk):
    if request.method == 'GET':
        diary = Diary.objects.filter(author_id = user_pk)
        serializer = DiarySerializer(diary, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        existing_diary = Diary.objects.filter(author_id=user_pk, date=datetime.date.today()).first()
        if existing_diary:
            return Response({"message": "하루에 하나의 다이어리만 작성할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DiaryCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author = request.user)
            User = get_user_model()
            user = get_object_or_404(User, pk = user_pk)
            user.stone += 5
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return 
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_diary(request, user_pk, diary_pk):
    if request.method == 'PUT':
        diary = get_object_or_404(Diary, id=diary_pk, author_id=user_pk)
        
        if request.user != diary.author:
            return Response({"message": "수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DiarySerializer(diary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        diary = get_object_or_404(Diary, id=diary_pk, author_id=user_pk)

        if request.user != diary.author:
            return Response({"message": "삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        diary.delete()
        return Response({"message": "다이어리가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
@api_view(['POST','PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def create_comment(request, diary_pk):
    user = request.user
    diary = get_object_or_404(Diary, pk = diary_pk)
    serializer = DiaryCommentSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = user, diary = diary)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)