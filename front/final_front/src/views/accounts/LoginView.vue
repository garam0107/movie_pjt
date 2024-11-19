<template>
    <div class="login-container">
        <h1>로그인</h1>
        <form @submit.prevent="login" class="login-form">
            <div class="form-group">
                <input type="text" v-model.trim="username" id="username" placeholder="사용자 이름" required class="form-input">
            </div>
            <div class="form-group">
                <input type="password" v-model.trim="password" id="password" placeholder="비밀번호" required class="form-input">
            </div>
            <button type="submit" class="submit-button">로그인</button>
        </form>
        <p class="not-a-member">아직 회원이 아니신가요? <a href="/signup" class="signup-link">회원가입</a></p>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref } from 'vue';
const username = ref(null);
const password = ref(null);
const store = useMovieStore();
const login = function() {
    const payload = {
        username: username.value,
        password: password.value
    };
    store.login(payload);
};
</script>

<style scoped>
.login-container {
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

.login-form {
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

.not-a-member {
    margin-top: 20px;
    font-size: 1rem;
    color: #666;
    font-family: 'Noto Sans KR', sans-serif;
}

.signup-link {
    color: #ff007f;
    text-decoration: none;
    font-weight: bold;
}

.signup-link:hover {
    text-decoration: underline;
}
</style>