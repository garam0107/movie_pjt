import { createRouter, createWebHistory } from 'vue-router'
import MovieMain from '@/views/MovieMainView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/main',
      name: 'main',
      component: MovieMain,
    },
  ],
})

export default router
