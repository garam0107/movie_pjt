import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'
import { parseQuery } from 'vue-router'

export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const API_URL = 'http://127.0.0.1:8000/'
  const detailMovie = ref([])
  const token = ref(null)
  const isAuthenticated = computed (() => !!token.value)
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
        console.log(res.data)
        token.value = res.data.key
        localStorage.setItem('token', res.data.key)
        router.push({ name: 'main'})
      })
      .catch(err => {
        console.log(err)
      })
  }

  // 회원가입
  const signup = function(payload){
    const { username, password1, password2, nickname, profile_image } = payload
    axios({
      method: 'post',
      url: `${API_URL}accounts/signup/`,
      data: {
        username, password1, password2, nickname, profile_image
      }
    })
      .then(res => {
        console.log(res.data)
        console.log('회원가입 완료')
        router.push({name: 'LoginView'})
      })
      .catch(err => {
        console.error('Error:', err.response ? err.response.data : err.message);
      })
  }

  const logout = function () {
    token.value = null
    localStorage.removeItem('token')
    router.push({ name: 'LoginView' })
  }

  const checkAuthentication = function () {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      token.value = storedToken;
    }
  }

  return { movies, API_URL, getMovies, getDetailMovie, detailMovie, login, token, signup
          , isAuthenticated, logout, checkAuthentication
   }
}, {persist:true})
