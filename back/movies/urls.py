from django.urls import path
from . import views
urlpatterns = [
    path('', views.main), # 영화 메인 페이지
    path('detail/<int:movie_pk>/', views.movie_detail), # 영화 상세 페이지
    path('detail/<int:movie_pk>/create_review/', views.create_review), # 영화 리뷰 작성
    path('detail/<int:movie_pk>/like', views.movie_like), # 영화 좋아요
    path('<int:movie_pk>/detail_review/', views.detail_review), # 영화 리뷰 더보기
    path('<int:movie_pk>/create_comment/', views.create_comment), # 영화 리뷰에 댓글 작성
]
