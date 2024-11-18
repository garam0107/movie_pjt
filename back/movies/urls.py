from django.urls import path
from . import views
urlpatterns = [
    path('', views.main), #영화 메인 페이지
    path('detail/<int:movie_pk>/', views.movie_detail), #영화 상세 페이지
]
