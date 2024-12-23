import os
import json
import re


from pathlib import Path


# 절대 경로로 변환해서 확인
# json_file_path = Path(__file__).resolve().parent/'updated_movies.json'
# print(f"확인할 파일 경로: {json_file_path}")
# if not json_file_path.exists():
#     print("Error: 파일이 존재하지 않습니다.")
# else:
#     print("파일이 정상적으로 존재합니다.")

# with open(json_file_path, encoding='utf-8') as f:
#     available_movies = json.load(f)

# print(available_movies)

# json_file_path2 = Path(__file__).resolve().parent.parent / 'movies' / 'fixtures' / 'movies.json'

# with open(json_file_path2, encoding='utf-8') as f:
#     available_movies2 = json.load(f)
# print(available_movies2)
# import json
# from pathlib import Path

# # 장르 매핑 딕셔너리 정의
# genre_mapping = {
#     12: "Adventure",
#     14: "Fantasy",
#     16: "Animation",
#     18: "Drama",
#     27: "Horror",
#     28: "Action",
#     35: "Comedy",
#     36: "History",
#     37: "Western",
#     53: "Thriller",
#     80: "Crime",
#     99: "Documentary",
#     878: "Science Fiction",
#     9648: "Mystery",
#     10402: "Music",
#     10749: "Romance",
#     10751: "Family",
#     10752: "War",
#     10770: "TV Movie"
# }

# # 절대 경로를 사용하여 JSON 파일 열기
# json_file_path = Path(__file__).resolve().parent.parent / 'movies' / 'fixtures' / 'movies.json'

# with open(json_file_path, encoding='utf-8') as f:
#     movies = json.load(f)

# # 각 영화의 genres ID를 이름으로 변환
# for movie in movies:
#     movie['fields']['genres'] = [genre_mapping[genre_id] for genre_id in movie['fields']['genres']]

# # 결과 확인을 위해 일부 출력
# for movie in movies[:3]:  # 예시로 처음 3개 영화만 출력
#     print(f"Title: {movie['fields']['title']}")
#     print(f"Genres: {', '.join(movie['fields']['genres'])}")
#     print("-" * 30)


# # 수정된 JSON 데이터를 파일로 저장
# with open('updated_movies.json', 'w', encoding='utf-8') as f:
#     json.dump(movies, f, ensure_ascii=False, indent=4)
from diaries.models import Diary
diary = Diary.objects.get(id=18)  # 특정 다이어리 가져오기
print(diary.recommend_reasons)  # JSONField 값 확인

# 테스트용 111