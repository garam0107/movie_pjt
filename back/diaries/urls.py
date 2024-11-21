from django.urls import path
from . import views
urlpatterns = [
    path('<str:user_username>/', views.user_diary), # 사용자 다이어리 페이지(조회, 생성)
    path('<str:user_username>/<int:diary_pk>/', views.update_diary), # 사용자 다이어리 페이지(수정, 삭제)
    path('<str:user_username>/comment/', views.create_comment), # 다이어리 댓글
    path('<str:user_username>/by_date/', views.diary_by_date), # 특정 날짜 다이어리 상세 내용 조회
]
