from django.urls import path
from . import views
urlpatterns = [
    path('<int:user_pk>/mypage/', views.mypage), # 마이 페이지(일기 작성,수정,삭제 가능, 사용자 상세 정보)
    path('<int:user_pk>/follow/', views.follow), # 팔로우 기능, 팔로우한 사람의 정보 가져오기)
    path('<int:user_pk>/update/', views.update),
]
