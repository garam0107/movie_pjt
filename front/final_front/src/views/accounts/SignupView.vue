<template>
    <div class="signup-container">

      <h1>회원가입</h1>
      <form @submit.prevent="submitForm" class="signup-form">
        <div class="form-group">
          <input type="text" v-model="username" id="username" placeholder="사용자 이름" required class="form-input">
        </div>
        
        <div class="form-group">
          <input type="email" v-model="email" id="email" placeholder="이메일" required class="form-input">
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
            <option value="profile_images/character_single1.jpg">Image 1</option>
            <option value="profile_images/character_single2.jpg">Image 2</option>
            <option value="profile_images/character_single3.jpg">Image 3</option>
            <option value="profile_images/character_single4.jpg">Image 4</option>
            <option value="profile_images/character_single5.jpg">Image 5</option>
            <option value="profile_images/character_single6.jpg">Image 6</option>
          </select>
        </div>
  
        <button type="submit" class="submit-button">회원가입</button>
      </form>
      <p class="already-member">이미 가입하셨나요? <a href="/login" class="login-link">로그인</a></p>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { ref } from 'vue';
    const username = ref('');
    const email = ref('');
    const password1 = ref('');
    const password2 = ref('');
    const nickname = ref('');
    const profile_image = ref('');
  
    const submitForm = () => {
      const formData = {
        username: username.value,
        email: email.value,
        password1: password1.value,
        password2: password2.value,
        nickname: nickname.value,
        profile_image: profile_image.value,
      };
  
      console.log("회원가입 데이터:", formData);
      axios.post('http://127.0.0.1:8000/accounts/signup/', formData) // 백엔드 회원가입 API 엔드포인트
      .then(response => {
        // 요청이 성공한 경우
        console.log('가입 성공:', response.data);
        alert('회원가입에 성공하셨습니다! 로그인 페이지로 이동합니다.');
      })
      .catch(error => {
        // 요청이 실패한 경우
        console.error('가입 실패:', error.response);
        if (error.response && error.response.data) {
          // 서버에서 전달된 에러 메시지가 있을 경우 이를 출력합니다.
          alert(`오류 발생: ${error.response.data.detail || '회원가입에 실패했습니다.'}`);
        } else {
          alert('회원가입에 실패했습니다. 다시 시도해주세요.');
        }
      });
    };
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
