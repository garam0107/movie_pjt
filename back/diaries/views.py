
import re
import json
import datetime
from pathlib import Path
from openai import OpenAI

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_list_or_404, get_object_or_404

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from .models import Diary
from movies.models import Movie
from .serializers import DiaryCreateSerializer, DiarySerializer,DiaryCommentSerializer
# Create your views here.



OPENAI_API_KEY = settings.OPENAI_API_KEY

json_file_path = Path(__file__).resolve().parent/'updated_movies.json'

def gpt_recommend(diary_text):
    try:
        client = OpenAI(
        api_key=OPENAI_API_KEY
        )
    except Exception as e:
        print(f'OpenAI API 호출 오류: {e}')

    try:
        with open(json_file_path, encoding='utf-8') as f:
            available_movies = json.load(f)
            print("파일을 성공적으로 읽었습니다.")
    except json.JSONDecodeError as e:
        print(f"JSON 파일을 파싱하는 도중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"파일을 여는 도중 예상치 못한 오류가 발생했습니다: {e}")
    # DB안에 있는 영화에서 검색해서 추천
    try:
        available_movies_str = "\n".join([f"- {movie['fields']['title']}: {', '.join(movie['fields']['genres'])}" for movie in available_movies])
    except KeyError as e:
        print(f'Key 오류: {e}')
    except Exception as e:
        print(f'데이터 변환 중 오류 : {e}')

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
    movies = re.findall(r"- Movie \d+: (.*?), \[(.*?)\]", answer)

    # movies 리스트의 길이를 확인하여 안전하게 접근
    if len(movies) >= 2:
        parsed_data['movies'] = {
            "title": [movies[0][0], movies[1][0]],
            "reason": [movies[0][1], movies[1][1]]
        }
    else:
        # 만약 movies 리스트의 길이가 충분하지 않다면 빈 값 또는 다른 처리를 추가
        parsed_data['movies'] = {
            "title": [movies[i][0] if i < len(movies) else "" for i in range(2)],
            "reason": [movies[i][1] if i < len(movies) else "" for i in range(2)]
        }

    # Diary Review 추출
    review_match = re.search(r"- Diary Review: (.+)", answer)
    if review_match:
        parsed_data['diary_review'] = review_match.group(1).strip()

    return parsed_data



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_diary(request, user_username):
    if request.method == 'GET':
        diary = Diary.objects.filter(author__username = user_username)
        serializer = DiarySerializer(diary, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        User = get_user_model()
        user = get_object_or_404(User, username = user_username)
        existing_diary = Diary.objects.filter(author=user, date=datetime.date.today()).first()
        if existing_diary:
            return Response({"message": "하루에 하나의 다이어리만 작성할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DiaryCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author = request.user)
            user.stone += 5
            user.save()
            user_data = serializer.data['content'] # 사용자가 쓴 일기 내용
            gpt_answer = gpt_recommend(user_data) # gpt의 답변
            gpt_json_answer = make_json(gpt_answer) # gpt 답변 json으로 가공
            data = {
                'create_diary' : serializer.data,
                'gpt_json_answer' : gpt_json_answer
            }
            # gpt가 영화를 추천한 이유를 딕셔너리 형태로 저장
            reasons = {'today_diary_review1' : gpt_json_answer['movies']['reason'][0],
                       'today_diary_review2' : gpt_json_answer['movies']['reason'][1]
                       }
            my_diary = Diary.objects.filter(author__username = user_username).first()
            if not my_diary:
                return JsonResponse({'message': '해당 사용자의 다이어리를 찾을 수 없습니다.'}, status= status.HTTP_404_NOT_FOUND)
            # diary에 gpt_comment 추가
            my_diary.gpt_comment = gpt_json_answer['diary_review']

            # recommend_movie와 Moive가 M:N 관계이기 때문에 Movie 객체를 가져와야 한다.
            # 제목을 통해 Moive 객체 가져오기

            movie_titles = gpt_json_answer['movies']['title']
            movies = Movie.objects.filter(title__in = movie_titles)

            for movie in movies:
                my_diary.recommend_movie.add(movie)

            # diary에 추천 이유 저장
            my_diary.recommend_reasons = reasons

            my_diary.save()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_diary(request, user_username, diary_pk):
    if request.method == 'PUT':
        diary = get_object_or_404(Diary, id=diary_pk, author__username = user_username)
        
        if request.user != diary.author:
            return Response({"message": "수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DiarySerializer(diary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        diary = get_object_or_404(Diary, id=diary_pk, author__username = user_username)

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



