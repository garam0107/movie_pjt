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
        console.log('정보확인',res.data)
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
            router.push({ name: 'MainDolDam' });
          })
          .catch(err => {
            console.log(err);
          });
      })
      .catch((err) => {
        // 로그인 실패 처리
        if (err.response && err.response.status === 400) {
          alert('아이디 혹은 비밀번호가 틀렸습니다.');
        } else if (err.request) {
          alert('서버 응답이 없습니다. 네트워크 상태를 확인해주세요.');
        } else {
          alert('로그인 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.');
        }
        console.error('로그인 요청 실패:', err);
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
    const storedToken = localStorage.getItem('token') || token.value;
  
    if (!storedToken) {
      console.warn("로그아웃 실패: 저장된 토큰이 없습니다.")
      clearAuthState(); // 클라이언트 상태 초기화
      return
    }
  
    axios({
      method: 'post',
      url: `${API_URL}accounts/logout/`,
      headers: {
        Authorization: `Token ${storedToken}`
      }
    })
      .then(() => {
        console.log("로그아웃 성공")
        clearAuthState() // 로그아웃 성공 시 상태 초기화
      })
      .catch(err => {
        console.error("로그아웃 실패:", err)
        clearAuthState()// 실패해도 클라이언트 상태 초기화
      })
  }
  // 다이어리 수정
  const updateDiary = (user_username, diary_pk, updateData) => {
    return axios({
      method: 'put',
      url: `${API_URL}diaries/${user_username}/${diary_pk}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: updateData
    })
    .then((res) => {
      console.log('성공', res.data);
      return res; // 응답을 반환해서 이후에 사용할 수 있도록 합니다.
    })
    .catch((err) => {
      console.log('실패', err);
      throw err; // 오류를 다시 던져서 호출자에서 이를 처리할 수 있게 합니다.
    });
  };
  
  

  // 다이어리 삭제
  const deleteDiary = (user_username,diary_pk) => {
    console.log(token.value)
    axios({
      method : 'delete',
      url: `${API_URL}diaries/${user_username}/${diary_pk}/`,
      headers :{
        Authorization : `Token ${token.value}`
      }
    }).then((res) => {
      console.log('성공',res.data)
    }).catch((err) => {
      console.log('실패', err)
      console.log(err.response.data)
    })
  }
  // 회원탈퇴 후 로그아웃
  const logout2 = function() {
    const storedToken = localStorage.getItem('token') || token.value;
  
    if (!storedToken) {
      console.warn("로그아웃 실패: 저장된 토큰이 없습니다.")
      clearAuthState(); // 클라이언트 상태 초기화
      return
    }
  
    axios({
      method: 'post',
      url: `${API_URL}accounts/logout/`,
      headers: {
        Authorization: `Token ${storedToken}`
      }
    })
      .then(() => {
        console.log("로그아웃 성공")
        clearAuthState2() // 로그아웃 성공 시 상태 초기화
      })
      .catch(err => {
        console.error("로그아웃 실패:", err)
        clearAuthState2()// 실패해도 클라이언트 상태 초기화
      })
  }

  // 클라이언트 상태 초기화 함수
  const clearAuthState = function() {
    token.value = null
    userId.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
    router.push({ name: 'LoginView' })
  }
  const clearAuthState2 = function() {
    token.value = null
    userId.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
    router.push({ name: 'MainDolDam' })
  }
  const checkAuthentication = function() {
    const storedToken = localStorage.getItem('token')
    const storedUserId = localStorage.getItem('userId')
  
    if (storedToken && storedUserId) {
      token.value = storedToken
      userId.value = storedUserId
    } else {
      clearAuthState() // 유효하지 않으면 상태 초기화
    }
  }
  const isAuthenticated = computed(() => !!token.value)

  return {
    movies,
    getMovies,
    getDetailMovie,
    detailMovie,
    login,
    signup,
    logout,
    logout2,
    checkAuthentication,
    isAuthenticated,
    token,
    userId,
    updateDiary,
    deleteDiary,
  }
}, { persist: true })
