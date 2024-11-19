<template>
    <div class="signup-container">

      <h1>회원가입</h1>
      <form @submit.prevent="signup" class="signup-form">
        <div class="form-group">
          <input type="text" v-model="username" id="username" placeholder="사용자 이름" required class="form-input">
        </div>
  
        <div class="form-group">
          <input type="password" v-model="password1" id="password1" placeholder="비밀번호" required class="form-input">
        </div>
  
        <div class="form-group">
          <input type="password" v-model="password2" id="password2" placeholder="비밀번호 확인" required class="form-input">
        </div>
  
        <div class="form-group">
          <input type="text" v-model="nickname" id="nickname" placeholder="별명" required class="form-input">
        </div>
  
        <div class="form-group">
          <label for="profile_image" class="profile-label">프로필 이미지 선택</label>
          <select v-model="profile_image" id="profile_image" required class="form-select">
            <option disabled value="">선택해 주세요</option>
            <option value="profile_images/profile1.jpg">Image 1</option>
            <option value="profile_images/profile2.jpg">Image 2</option>
            <option value="profile_images/profile3.jpg">Image 3</option>
            <option value="profile_images/profile4.jpg">Image 4</option>
            <option value="profile_images/profile5.jpg">Image 5</option>
            <option value="profile_images/profile6.jpg">Image 6</option>
          </select>
        </div>
  
        <button type="submit" class="submit-button">회원가입</button>
      </form>
      <p class="already-member">이미 가입하셨나요? <a href="/login" class="login-link">로그인</a></p>
    </div>
  </template>
  
  <script setup>
  import { useMovieStore } from '@/stores/counter';
  import { ref } from 'vue';
  const store = useMovieStore()
    const username = ref(null);
    // const email = ref(null);
    const password1 = ref(null);
    const password2 = ref(null);
    const nickname = ref(null);
    const profile_image = ref(null);

  const signup = function() {
    const payload = {
      username: username.value,
      // email: email.value,
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
      margin-bottom: 5px;
      color: #555;
      display: block;
      text-align: left;
    }

    .form-select {
      width: 100%;
      padding: 15px;
      font-size: 1rem;
      border: 1px solid #ddd;
      border-radius: 10px;
      outline: none;
      background-color: #fafafa;
      cursor: pointer;
    }

    .form-select:focus {
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
  </style>
