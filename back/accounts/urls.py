from django.urls import path
from . import views
urlpatterns = [
    path('<int:user_pk>/mypage/', views.mypage), # 마이 페이지
]
