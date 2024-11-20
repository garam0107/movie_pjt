import re
import json
import datetime
from pathlib import Path
from openai import OpenAI

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_list_or_404, get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from .models import Diary
from .serializers import DiaryCreateSerializer, DiarySerializer,DiaryCommentSerializer
# Create your views here.



OPENAI_API_KEY = settings.OPENAI_API_KEY
json_file_path = Path(__file__).resolve().parent.parent / 'movies' / 'fixtures' / 'movies.json'

def gpt_recommend(diary_text):
    client = OpenAI(
    api_key=OPENAI_API_KEY
    )
    with open(json_file_path, encoding='utf-8') as f: available_movies = json.load(f)
    # DB안에 있는 영화에서 검색해서 추천
    available_movies_str = "\n".join([f"- {movie['title']}: {', '.join(movie['genres'])} - {movie['description']}" for movie in available_movies])

    # 사용자가 작성한 일기 데이터 예시

    # 프롬프트 작성
    messages = [
        {"role": "system", "content": "You are an assistant that helps users analyze their emotions from diary entries and provides movie recommendations. All responses should be in Korean."},
        {"role": "user", "content": f"""
    Here is a diary entry written by the user: "{diary_text}"

    Based on the following available movies, analyze the emotion in the diary entry and recommend two movies from the list: 
    {available_movies_str}

    1. Analyze the emotion in this diary entry. If the detected emotion is one of Joy, Sadness, Anger, Melancholy, Calm, or Excitement, provide a movie recommendation based on the genres associated with that emotion.
    - Emotion-based movie genres:
    Joy: Comedy (35), Animation (16), Family (10751), Music (10402), Romance (10749), Adventure (12)
    Sadness: Drama (18), Romance (10749), History (36)
    Anger: Action (28), Crime (80), Thriller (53), War (10752)
    Melancholy: Drama (18), Documentary (99), Mystery (9648)
    Calm: Documentary (99), Family (10751), Fantasy (14)
    Excitement: Adventure (12), Romance (10749), Animation (16), Music (10402), Science Fiction (878)

    2. If the detected emotion is not among the six defined categories, analyze it freely and recommend a movie based on the detected emotion.

    3. Provide two movie recommendations: one that matches the detected emotion and one that is the opposite to help balance the user's mood.

    All responses should be in Korean. Please write Emotion in Korean
    Output format:
    - Detected Emotion: [Emotion]
    - Movie 1: [Movie Title], [Reason for recommendation]
    - Movie 2: [Movie Title], [Reason for recommendation]
    - Diary Review: [A short review of the diary entry]
    """}
    ]

    # ChatCompletion 엔드포인트 호출하여 감정 분석 및 영화 추천 받기

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 사용할 모델 이름
        messages=messages,
        max_tokens=500,  # 응답에서 사용할 최대 토큰 수
        temperature=0.85  # 응답의 다양성을 위한 온도 설정
    )

    # 응답 내용 출력
    answer = response.choices[0].message.content
    return answer





def make_json(answer):
    parsed_data = {}
    # 감정 추출
    emotion_match = re.search(r"- Detected Emotion: (.+)", answer)
    if emotion_match:
        parsed_data['detected_emotion'] = emotion_match.group(1).strip()

    # Movie 1과 Movie 2 정보 추출
    movies = re.findall(r"- Movie \d+: \"(.+)\", \[(.+)\]", answer)
    parsed_data['movies'] = [{'title': movie[0], 'reason': movie[1]} for movie in movies]

    # Diary Review 추출
    review_match = re.search(r"- Diary Review: \[(.+)\]", answer)
    if review_match:
        parsed_data['diary_review'] = review_match.group(1).strip()

    return parsed_data



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
            user_data = serializer.data['content'] # 사용자가 쓴 일기 내용
            gpt_answer = gpt_recommend(user_data) # gpt의 답변
            gpt_json_answer = make_json(gpt_answer) # gpt 답변 json으로 가공
            data = {
                'create_diary' : serializer.data,
                'gpt_json_answer' : gpt_json_answer
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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