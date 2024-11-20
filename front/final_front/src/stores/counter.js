import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useMovieStore = defineStore('movie', () => {
  const movies = ref([]);
  const API_URL = 'http://127.0.0.1:8000/';
  const detailMovie = ref([]);
  const token = ref(localStorage.getItem('token') || null);
  const userData = ref([]);
  const userId = ref(localStorage.getItem('userId') || null);

  const getMovies = function() {
    axios({
      method: 'get',
      url: `${API_URL}movies/`
    })
      .then(res => {
        movies.value = res.data;
      })
      .catch(err => console.log(err));
  };

  const getDetailMovie = (id) => {
    axios({
      method: 'get',
      url: `${API_URL}movies/detail/${id}/`
    })
      .then(res => {
        detailMovie.value = res.data;
      })
      .catch(err => console.log(err));
  };

  // 로그인
  const login = function(payload) {
    const { username, password } = payload;
    axios({
      method: 'post',
      url: `${API_URL}accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        token.value = res.data.key;
        localStorage.setItem('token', res.data.key);

        // 사용자 정보 요청
        axios({
          method: 'get',
          url: `${API_URL}accounts/user/`,
          headers: {
            Authorization: `Token ${res.data.key}`
          }
        })
        .then(userRes => {
          userId.value = userRes.data.username;
          localStorage.setItem('userId', userRes.data.username);
          router.push({ name: 'main' });
        })
        .catch(err => {
          console.log(err);
        });
      })
      .catch(err => {
        console.log(err);
      });
  };

  // 회원가입
  const signup = function(payload){
    const { username, password1, password2, nickname, profile_image } = payload;
    axios({
      method: 'post',
      url: `${API_URL}accounts/signup/`,
      data: {
        username, password1, password2, nickname, profile_image
      }
    })
      .then(res => {
        console.log('회원가입 완료');
        router.push({name: 'LoginView'});
      })
      .catch(err => {
        console.error('Error:', err.response ? err.response.data : err.message);
      });
  };

  // 로그아웃
  const logout = function() {
    axios({
      method: 'post',
      url: `${API_URL}accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        token.value = null;
        userId.value = null;
        localStorage.removeItem('token');
        localStorage.removeItem('userId');
        router.push({ name: 'LoginView' });
      })
      .catch(err => {
        console.error('로그아웃 실패:', err);
      });
  };
  
  const checkAuthentication = function () {
    const storedToken = localStorage.getItem('token');
    const storedUserId = localStorage.getItem('userId');
    if (storedToken) {
      token.value = storedToken;
      userId.value = storedUserId;
    }
  };

  const isAuthenticated = computed(() => !!token.value);

  return {
    movies,
    getMovies,
    getDetailMovie,
    detailMovie,
    login,
    signup,
    logout,
    checkAuthentication,
    isAuthenticated,
    token,
    userId
  };
}, { persist: true });
