from django.urls import path
from . import views
urlpatterns = [
    path('<int:user_pk>/', views.user_diary), # 사용자 다이어리 페이지

]
