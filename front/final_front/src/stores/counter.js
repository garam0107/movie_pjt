import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const API_URL = 'http://127.0.0.1:8000/'
  const detailMovie = ref([])
  const token = ref(null)
  const getMovies = function() {
    axios ({
      method: 'get',
      url: `${API_URL}movies/`
    })
      .then(res => {
        // console.log(res.data)
        movies.value = res.data
      })
      .catch(err => console.log(err))
  }

  const getDetailMovie = (id) => {
    axios({
      method: 'get',
      url: `${API_URL}movies/detail/${id}/`
    })
      .then(res => {
        detailMovie.value = res.data
      })
      .catch(err => console.log(err))
  }

  // 로그인
  const login = function(payload) {
    const username = payload.username
    const password = payload.password
    axios({
      method: 'post',
      url: `${API_URL}accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        token.value = res.data.key
        router.push({ name: 'main'})
      })
      .catch(err => {
        console.log(err)
      })
  }
  return { movies, API_URL, getMovies, getDetailMovie, detailMovie, login, token }
}, {persist:true})
