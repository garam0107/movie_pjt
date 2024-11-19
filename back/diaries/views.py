from django.shortcuts import render, get_list_or_404, get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from .models import Diary
from .serializers import DiaryDetailSerializer, DiarySerializer
# Create your views here.
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_diary(request, user_pk):
    if request.method == 'GET':
        diary = Diary.objects.filter(author = user_pk)
        serializer = DiarySerializer(diary, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass    