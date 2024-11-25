
import re
import json
import datetime
from datetime import datetime as dt
from pathlib import Path
from openai import OpenAI

from django.db import transaction
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
from .serializers import DiaryCreateSerializer, DiarySerializer,DiaryCommentSerializer,DiaryDetailSerializer,GptAnswerSerializer,OptimizedDiarySerializer
# Create your views here.




OPENAI_API_KEY = "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"

# OPENAI_API_KEY = settings.OPENAI_API_KEY
json_file_path = Path(__file__).resolve().parent/'updated_movies.json'

def clean_movie_title(title):
    # 이스케이프 문자, 불필요한 특수문자 제거 (`:`, `-` 등은 남겨둠)
    cleaned_title = re.sub(r'[\\*"》<>]', '', title)  # \, *, ", 》, <, > 제거
    cleaned_title = re.sub(r"^'+|'+$", '', cleaned_title)  # 제목 앞뒤의 단일 따옴표 제거
    cleaned_title = cleaned_title.strip()  # 앞뒤 공백 제거
    return cleaned_title

def gpt_recommend(diary_text):
    try:
        client = OpenAI(
        api_key=OPENAI_API_KEY
        )
    except Exception as e:
        print(f'OpenAI API 호출 오류: {e}')
        return None

    try:
        with open(json_file_path, encoding='utf-8') as f:
            available_movies = json.load(f)
            # 제목을 정리하여 불필요한 특수 문자가 추가되지 않도록 처리
            for movie in available_movies:
                movie['fields']['title'] = clean_movie_title(movie['fields']['title'])
            print("파일을 성공적으로 읽고 제목을 정리했습니다.")
    except json.JSONDecodeError as e:
        print(f"JSON 파일을 파싱하는 도중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"파일을 여는 도중 예상치 못한 오류가 발생했습니다: {e}")

    # DB안에 있는 영화에서 검색해서 추천
    try:
        available_movies_str = "\n".join([f"- {clean_movie_title(movie['fields']['title'])}: {', '.join(movie['fields']['genres'])}" for movie in available_movies])
    except KeyError as e:
        print(f'Key 오류: {e}')
        return None
    except Exception as e:
        print(f'데이터 변환 중 오류 : {e}')
        return None


        # 프롬프트 작성
    messages = [
    {"role": "system", "content": "You are an assistant that helps users analyze their emotions from diary entries and provides personalized movie recommendations. All responses should be in Korean, and they should sound empathetic and supportive, as if you're talking to a close friend."},
    {"role": "user", "content": f"""
    Here is a diary entry written by the user: "{diary_text}"

    Based on the following available movies, analyze the emotion in the diary entry and recommend two movies from the list:
    {available_movies_str}

    1. Analyze the emotion in this diary entry. If the detected emotion is one of Joy, Sadness, Anger, Melancholy, Calm, or Excitement, provide a movie recommendation based on the genres associated with that emotion.
    - Emotion-based movie genres (with additional genres for variety):
    Joy: Comedy (35), Animation (16), Family (10751), Music (10402), Romance (10749), Adventure (12), Action (28), Fantasy (14)
    Sadness: Drama (18), Romance (10749), History (36), Family (10751)
    Anger: Action (28), Crime (80), Thriller (53), War (10752), Adventure (12)
    Melancholy: Drama (18), Documentary (99), Mystery (9648), Romance (10749)
    Calm: Documentary (99), Family (10751), Fantasy (14), Music (10402), Science Fiction (878)
    Excitement: Adventure (12), Romance (10749), Animation (16), Music (10402), Science Fiction (878), Action (28)

    2. If the detected emotion is not among the six defined categories, analyze it freely and recommend a movie based on the detected emotion.

    3. Provide two movie recommendations: one that matches the detected emotion and one that contrasts with it to help balance the user's mood. Avoid recommending movies that have been previously recommended too frequently to ensure variety. Try to provide lesser-known but well-received movies where appropriate.
    - Please make sure that each recommendation includes a warm and empathetic explanation. Try to make it feel like you understand the user's emotions and why the suggested movie would be comforting or inspiring to them.

    4. Write a detailed diary review with a length of 4-6 sentences. The review should focus on understanding the user's feelings, recognizing their efforts or struggles, and providing a comforting or insightful comment. Make it feel like you're truly listening to their story and offering thoughtful support.
    5. You can analyze your emotions in various ways. You must write the detected emotion in Korean and describe it in a natural way, not in English.
    
    All responses should be in Korean. Please write 'Detected Emotion', 'Movie 1', 'Movie 2', and 'Diary Review' labels in English, while the actual content should be in Korean.
    Output format:
   - Detected Emotion: [Emotion]
    - Movie 1: [Movie Title] - [Reason for recommendation]
    - Movie 2: [Movie Title] - [Reason for recommendation]
    - Diary Review: [A review of the diary entry]
    Please stop recommending movies 'inside out'
    Please remember to be empathetic and supportive in your responses, and ensure that each recommendation is diverse, considering both popular and less well-known titles for variety.
    """}
]

    # ChatCompletion 엔드포인트 호출하여 감정 분석 및 영화 추천 받기
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용할 모델 이름
            messages=messages,
            max_tokens=500,  # 응답에서 사용할 최대 토큰 수
            temperature=0.9,   # 응답의 다양성을 위한 온도 설정
            top_p=0.8
        )

        # 응답 내용 출력
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        print(f'응답 오류 :{e}')
        return None




def make_json(answer):
    parsed_data = {}

    # 감정 추출
    emotion_match = re.search(r"- Detected Emotion: (.+)", answer)
    if emotion_match:
        parsed_data['detected_emotion'] = emotion_match.group(1).strip()

    # Movie 1과 Movie 2 정보 추출 (제목과 이유를 정확히 분리)
    movies = re.findall(r"- Movie \d+: (.*?) - (.*?)$", answer, re.MULTILINE)

    # movies 리스트의 길이를 확인하여 안전하게 접근
    if len(movies) >= 2:
        parsed_data['movies'] = {
            "title": [clean_movie_title(movies[0][0]), clean_movie_title(movies[1][0])],
            "reason": [movies[0][1].strip(), movies[1][1].strip()]
        }
    else:
        # 만약 movies 리스트의 길이가 충분하지 않다면 빈 값 또는 다른 처리를 추가
        parsed_data['movies'] = {
            "title": [clean_movie_title(movies[i][0]) if i < len(movies) else "" for i in range(2)],
            "reason": [movies[i][1].strip() if i < len(movies) else "" for i in range(2)]
        }

    # Diary Review 추출
    review_match = re.search(r"- Diary Review: (.+)", answer, re.DOTALL)
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

        today = datetime.date.today()
        existing_diary = Diary.objects.filter(author=user, date=datetime.date.today()).first()
        if existing_diary:
            return Response({"message": "하루에 하나의 다이어리만 작성할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        requested_data = request.data.get('date')
        if requested_data and requested_data != str(today):
            return Response({"message" : "당일에만 다이어리를 작성할 수 있습니다."})
        serializer = DiaryCreateSerializer(data = request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        try:
            with transaction.atomic():

                diary = serializer.save(author = request.user, date = today)
                user.stone += 5
                user.save()
                user_data = serializer.data['content'] # 사용자가 쓴 일기 내용
                gpt_answer = gpt_recommend(user_data) # gpt의 답변
                print(gpt_answer)
                gpt_json_answer = make_json(gpt_answer) # gpt 답변 json으로 가공


                # gpt가 분석한 감정 저장
                diary.analysis_emotion = gpt_json_answer['detected_emotion']
                # gpt가 영화를 추천한 이유를 딕셔너리 형태로 저장
                reasons = {'today_diary_review1' : gpt_json_answer['movies']['reason'][0],
                        'today_diary_review2' : gpt_json_answer['movies']['reason'][1]
                        }

                # diary에 gpt_comment 추가
                if gpt_json_answer['diary_review']:
                    diary.gpt_comment = gpt_json_answer['diary_review']
                else:
                    pass
                # recommend_movie와 Moive가 M:N 관계이기 때문에 Movie 객체를 가져와야 한다.
                # 제목을 통해 Moive 객체 가져오기

                movie_titles = gpt_json_answer['movies']['title']
                movies = Movie.objects.filter(title__in = movie_titles)
                
                for movie in movies:
                    diary.recommend_movie.add(movie)
                # 추천 영화 제목 저장
                diary.recommend_movie_titles = gpt_json_answer['movies']['title']
                # diary에 추천 이유 저장
               
                diary.recommend_reasons = reasons
                diary.save()
                data = GptAnswerSerializer(diary).data
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "다이어리 작성 중 문제가 발생했습니다.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_diary(request, user_username, diary_pk):
    # if request.method == 'PUT':
    #     diary = get_object_or_404(Diary, id=diary_pk, author__username = user_username)
        
    #     if request.user != diary.author:
    #         return Response({"message": "수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    #     serializer = DiarySerializer(diary, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    diary = get_object_or_404(Diary, id=diary_pk, author__username=user_username)

    # 권한 확인
    if request.user != diary.author:
        return Response({"message": "수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = DiarySerializer(diary, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                # 다이어리 내용 업데이트
                serializer.save()

                # GPT 추천 재실행
                try:
                    updated_content = serializer.validated_data.get('content', diary.content)
                    gpt_answer = gpt_recommend(updated_content)  # GPT 추천 호출
                    print(gpt_answer)
                    gpt_json_answer = make_json(gpt_answer)  # 응답 JSON으로 가공

                    # 감정 및 추천 업데이트
                    diary.analysis_emotion = gpt_json_answer['detected_emotion']
                    reasons = {
                        'today_diary_review1': gpt_json_answer['movies']['reason'][0],
                        'today_diary_review2': gpt_json_answer['movies']['reason'][1],
                    }
                    diary.gpt_comment = gpt_json_answer.get('diary_review', diary.gpt_comment)

                    # 기존 추천 영화 제거
                    diary.recommend_movie.clear()

                    # 새로운 추천 영화 추가
                    movie_titles = gpt_json_answer['movies']['title']
                    movies = Movie.objects.filter(title__in=movie_titles)
                    for movie in movies:
                        diary.recommend_movie.add(movie)

                    # 추천 데이터 업데이트
                    diary.recommend_movie_titles = gpt_json_answer['movies']['title']
                    diary.recommend_reasons = reasons
                    diary.save()

                except Exception as e:
                    return Response(
                        {"message": "GPT 추천 업데이트 중 문제가 발생했습니다.", "error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                # 성공 응답
                updated_data = DiaryDetailSerializer(diary).data
                return Response(updated_data, status=status.HTTP_200_OK)

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




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diary_by_date(request, user_username):
    """
    특정 날짜의 다이어리 확인
    """
    date = request.query_params.get('date')
    if not date:
        return Response({"message": "날짜가 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    diary = Diary.objects.filter(author__username=user_username, date=date).first()
    if diary:
        serializer = DiaryDetailSerializer(diary)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"exists": False}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_month_diaries(request, user_username, year, month):
    User = get_user_model()
    author = get_object_or_404(User, username=user_username)

    # 날짜 계산 개선
    start_date = dt(year, month, 1)
    if month < 12:
        end_date = dt(year, month + 1, 1)
    else:
        end_date = dt(year + 1, 1, 1)

    # 해당 월의 다이어리 데이터를 필터링
    diaries = Diary.objects.filter(author=author, date__gte=start_date, date__lt=end_date)

    # 빈 리스트로 응답
    if not diaries.exists():
        return Response([], status=status.HTTP_200_OK, content_type='application/json')

    # 월별 데이터를 위한 시리얼라이저 사용
    serializer = OptimizedDiarySerializer(diaries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')