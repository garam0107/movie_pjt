<template>
    <header class="watchapedia-header">
      <div class="logo-nav-container">
        <div class="logo">
          <img src="@/assets/movie_logo.png" alt="logo_img" class="logo_img">
        </div>
        <nav class="nav-links">
          <RouterLink to="/"class="nav-link">홈</RouterLink>
          <RouterLink to="/main"class="nav-link">영화</RouterLink>
          <RouterLink v-if="userId" :to="{ name: 'MyPageView', params: { user_id: userId } }" class="nav-link">마이페이지</RouterLink>
        </nav>
      </div>
      <div class="header-right">
        <input type="text" placeholder="콘텐츠, 인물, 컬렉션, 유저를 검색해보세요" class="search-input" />
        <RouterLink v-if="!userId" :to="{name: 'LoginView'}"><button class="signup-button">로그인</button></RouterLink>
        <RouterLink v-if="!userId" :to="{name: 'SignupView'}"><button class="signup-button">회원가입</button></RouterLink>
        <button  v-if="userId" @click="logout" class="signup-button">로그아웃</button>
      </div>
    </header>
  </template>
  
  <script setup>
import { useMovieStore } from '@/stores/counter';
import { computed, onMounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
const store = useMovieStore()
const userId = computed(() => store.userId)
const logout = () => {
  store.logout()
}

  </script>
  
  <style scoped>

@import url('https://fonts.googleapis.com/css2?family=Hahmlet:wght@100..900&family=Noto+Sans+KR:wght@100..900&family=Noto+Serif+KR:wght@200..900&display=swap');
  .watchapedia-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    border-bottom: 1px solid #ddd;
    background-color: #fff;
    font-family: "Noto Sans KR", sans-serif;
    max-width: 1400px;
    margin: 0 auto;
    box-sizing: border-box;
    flex-wrap: nowrap;
    width: 80%;
  }
  
  .logo-nav-container {
    display: flex;
    align-items: center;
  }
  
  .logo_img {
    width: 170px; 
    max-width: 100%; 
    height: auto; 
  }
  
  .nav-links {
    display: flex;
    gap: 15px; 
    margin-left: 20px; 
  }
  
  .nav-link {
    text-decoration: none;
    color: #333;
    font-size: 19px;
  }
  
  .nav-link:hover {
    color: dimgray; 
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 15px;
    flex-shrink: 1;
  }
  
  .search-input {
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    width: 250px;
    transition: width 0.3s ease;
  }
  
  .login-link {
    text-decoration: none;
    color: #333;
    font-size: 16px;
  }
  
  .signup-button {
    padding: 5px 15px;
    border: 1px solid #333;
    background-color: transparent;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .signup-button:hover {
    background-color: lightgrey;
    color: #fff;
    border: 1px solid lightgrey;
  }
  
  /* 반응형 스타일 */
  @media (max-width: 768px) {
    .search-input {
      width: 150px;
    }
  
    .nav-links {
      gap: 5px;
    }
  
    .header-right {
      gap: 10px;
    }
  }
  /* 반응형 스타일 */
  @media (max-width: 1024px) {
    .search-input {
      width: 200px; /* 화면이 좁아질 때 검색창 너비 조정 */
    }
  
    .signup-button {
      padding: 5px 10px; /* 버튼 크기 조정 */
    }
  }
  
  @media (max-width: 768px) {
    .logo_img {
      width: 120px; /* 로고 크기 줄이기 */
    }
  
    .search-input {
      width: 150px; /* 검색창 너비 줄이기 */
    }
  
    .nav-links {
      gap: 5px; /* 내비게이션 링크 간격 줄이기 */
    }
  
    .header-right {
      gap: 5px; /* 헤더 오른쪽 요소 간격 줄이기 */
    }
  
    .signup-button {
      padding: 4px 8px; /* 버튼 크기 줄이기 */
      font-size: 14px; /* 글자 크기 줄이기 */
    }
  }
  
  @media (max-width: 480px) {
    .search-input {
      display: none; /* 매우 작은 화면에서는 검색창 숨기기 */
    }
  
    .header-right {
      flex-direction: row; /* 여전히 한 줄 유지 */
    }
  }
  
  </style>
  