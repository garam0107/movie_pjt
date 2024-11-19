from django.urls import path
from . import views
urlpatterns = [
    path('<int:user_pk>/', views.user_diary), # 사용자 다이어리 페이지(조회, 생성)
    path('<int:user_pk>/<int:diary_pk>/', views.update_diary), # 사용자 다이어리 페이지(수정, 삭제)
    path('<int:diary_pk>/comment/', views.create_comment) # 다이어리 댓글
]
