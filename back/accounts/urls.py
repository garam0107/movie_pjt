from django.urls import path
from . import views
urlpatterns = [
    path('<str:user_username>/mypage/', views.mypage), # 마이 페이지
    path('<str:user_username>/follow/', views.follow), # 팔로우 기능, 팔로우한 사람의 정보 가져오기)
    path('<str:user_username>/update/', views.update), # 회원 정보 수정
    path('all/', views.top_users_by_stone), 
    path('check-username/', views.check_username, name='check-username'), # 전체 회원 정보 들고오기
    path('delete/', views.delete) # 회원 탈퇴
]
