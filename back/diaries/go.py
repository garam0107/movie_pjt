import os
print(f'현재 작업 디렉토리:{os.getcwd()}')

from pathlib import Path

# 절대 경로로 변환해서 확인
json_file_path = Path(__file__).resolve().parent.parent / 'movies' / 'fixtures' / 'movies.json'

print(f"확인할 파일 경로: {json_file_path}")
if not json_file_path.exists():
    print("Error: 파일이 존재하지 않습니다.")
else:
    print("파일이 정상적으로 존재합니다.")

print(json_file_path)