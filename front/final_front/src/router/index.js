import { createRouter, createWebHistory } from 'vue-router'
import MovieMainView from '@/views/MovieMainView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import SignupView from '@/views/accounts/SignupView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import MyPageView from '@/views/mypage/MyPageView.vue'
import { useMovieStore } from '@/stores/counter'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 영화 메인
    {
      path: '/main',
      name: 'main',
      component: MovieMainView,
    },
    // 영화 디테일
    {
      path: '/movie/:movie_id',
      name: 'detail',
      component: MovieDetailView
    },
    // 회원가입
    {
      path: '/signup',
      name: 'SignupView',
      component: SignupView
    },
    // 로그인
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView
    },
    // 마이페이지
    // {
    //   path: '/mypage/:user_id',
    //   name: 'MyPageView',
    //   component: MyPageView
    // }
  ],
})

export default router
