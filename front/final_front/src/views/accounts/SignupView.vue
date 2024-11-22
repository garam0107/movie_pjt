<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="signup" class="signup-form">
      <div class="form-group">
        <input
          type="text"
          v-model="username"
          id="username"
          placeholder="ID"
          required
          class="form-input"
          @blur="checkUsername"
        >
        <p v-if="usernameStatus === 'available'" class="username-available">사용 가능한 ID입니다.</p>
        <p v-else-if="usernameStatus === 'unavailable'" class="username-unavailable">이미 사용 중인 ID입니다.</p>
      </div>
      <div class="form-group">
        <input type="password" v-model="password1" id="password1" placeholder="비밀번호" required class="form-input">
      </div>

      <div class="form-group">
        <input type="password" v-model="password2" id="password2" placeholder="비밀번호 확인" required class="form-input">
        <p v-if="passwordMatchStatus === 'match'" class="password-match">비밀번호가 일치합니다.</p>
        <p v-else-if="passwordMatchStatus === 'not-match'" class="password-not-match">비밀번호가 일치하지 않습니다.</p>
      </div>

      <div class="form-group">
        <input type="text" v-model="nickname" id="nickname" placeholder="닉네임" required class="form-input">
      </div>

      <!-- 프로필 이미지 선택 -->
      <div class="form-group profile-selection">
        <p class="profile-label">프로필 이미지 선택</p>
        <div class="profile-images">
          <label v-for="(image, index) in profileOptions" :key="index" class="profile-option">
            <input 
              type="radio" 
              :value="image.value" 
              v-model="profile_image"
              name="profile_image"
            >
            <img :src="image.src" :alt="image.label" class="profile-img" :title="image.label">
          </label>
          <label class="profile-option">
            <input 
              type="radio" 
              value="" 
              v-model="profile_image"
              name="profile_image"
            >
            <!-- <img :src="defaultProfileImageUrl" alt="기본 이미지" class="profile-img default-img" title="기본 이미지 (선택 안함)"> -->
          </label>
        </div>
      </div>

      <button type="submit" class="submit-button">회원가입</button>
    </form>
    <p class="already-member">이미 가입하셨나요? <a href="/login" class="login-link">로그인</a></p>
  </div>
</template>
  
<script setup>
import { useMovieStore } from '@/stores/counter';
import { computed, ref, watch } from 'vue';
// import defaultProfileImageUrl from '@/assets/default_profile.jpg';
import axios from 'axios';
const store = useMovieStore()
const username = ref(null);
const usernameStatus = ref('')
// const email = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const nickname = ref(null);
const profile_image = ref(null);

// 프로필 이미지 옵션들
const profileOptions = [
{ value: "profile_images/profile1.jpg", src: new URL('@/assets/profile_images/profile1.jpg', import.meta.url).href, label: "Image 1" },
{ value: "profile_images/profile2.jpg", src: new URL('@/assets/profile_images/profile2.jpg', import.meta.url).href, label: "Image 2" },
{ value: "profile_images/profile3.jpg", src: new URL('@/assets/profile_images/profile3.jpg', import.meta.url).href, label: "Image 3" },
{ value: "profile_images/profile4.jpg", src: new URL('@/assets/profile_images/profile4.jpg', import.meta.url).href, label: "Image 4" },
{ value: "profile_images/profile5.jpg", src: new URL('@/assets/profile_images/profile5.jpg', import.meta.url).href, label: "Image 5" },
{ value: "profile_images/profile6.jpg", src: new URL('@/assets/profile_images/profile6.jpg', import.meta.url).href, label: "Image 6" },
{ value: "profile_images/default_profile.jpg", src: new URL('@/assets/profile_images/default_profile.jpg', import.meta.url).href, label: "Image 7"}
];

// 비밀번호 일치 여부 확인
const passwordMatchStatus = computed(() => {
  if (!password1.value || !password2.value) {
    return ''
  }
  return password1.value === password2.value ? 'match' : 'not-match'
})

// 아이디 확인
watch(username, (newVal) => {
  if (newVal) checkUsername()
})

const checkUsername = () => {
  if (username.value) {
    axios.get('http://127.0.0.1:8000/accounts/check-username/', {
      params: { username: username.value }
    })
    .then((response) => {
      if (response.data.available) {
        usernameStatus.value = 'available'
      } else {
        usernameStatus.value = 'unavailable'
      }
    })
    .catch((error) => {
      console.error('ID 중복 확인 실패:', error)
      usernameStatus.value = null
    })
  }
}

const signup = function() {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    profile_image: profile_image.value
  }
  store.signup(payload)
}
</script>
  
<style scoped>
.signup-container {
  width: 100%;
  max-width: 400px;
  margin: 40px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
  text-align: center;
}

h1 {
  font-size: 2rem;
  margin-bottom: 30px;
  color: gray;
  font-weight: 700;
  font-family: 'Noto Sans KR', sans-serif;
}

.signup-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.form-group {
  width: 100%;
}

.form-input {
  width: 80%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafafa;
}

.form-input:focus {
  border-color: #ff007f;
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.3);
}

.profile-label {
  font-weight: bold;
  margin-bottom: 10px;
  color: #555;
  display: block;
}

.profile-selection {
  width: 100%;
  text-align: left;
}

.profile-images {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
  justify-content: center;
}

.profile-option {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd;
  cursor: pointer;
  transition: border-color 0.3s;
}

.profile-img:hover {
  border-color: #ff007f;
}

input[type="radio"] {
  display: none; /* 기본 라디오 버튼 숨기기 */
}

input[type="radio"]:checked + .profile-img {
  border-color: #ff007f; /* 선택된 이미지 강조 */
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.3);
}

.no-image {
  display: block;
  font-size: 0.9rem;
  padding: 15px 10px;
  background-color: #fafafa;
  border-radius: 10px;
  border: 2px solid #ddd;
  cursor: pointer;
}

input[type="radio"]:checked + .no-image {
  border-color: #ff007f;
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.3);
}

.submit-button {
  width: 100%;
  padding: 15px;
  background: gray;
  color: #fff;
  font-size: 1.3rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s;
  margin-top: 20px;
  font-weight: bold;
}

.submit-button:hover {
  background: #e00070;
  transform: translateY(-2px);
}

.submit-button:active {
  transform: translateY(0);
}

.already-member {
  margin-top: 20px;
  font-size: 1rem;
  color: #666;
  font-family: 'Noto Sans KR', sans-serif;
}

.login-link {
  color: #ff007f;
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}

.password-not-match{
  color: red;
 
}

.password-match{
  color: blue;
  margin-bottom: 0
}

.username-available {
  color: green;
  font-size: 0.9rem;
  margin-bottom: 0;
}

.username-unavailable {
  color: red;
  font-size: 0.9rem;
  margin-bottom: 0;
}
</style>
