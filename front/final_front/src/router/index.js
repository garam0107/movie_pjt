import { createRouter, createWebHistory } from 'vue-router'
import MovieMainView from '@/views/MovieMainView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/main',
      name: 'main',
      component: MovieMainView,
    },
    {
      path: '/movie/:movie_id',
      name: 'detail',
      component: MovieDetailView
    },
  ],
})

export default router
