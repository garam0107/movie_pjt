<script setup>
import { RouterLink, RouterView } from 'vue-router';
import Footer from './components/common/Footer.vue';
import Header from './components/common/Header.vue';
</script>

<template>
  <Header />
  <div class="layout-container">
    <main class="container">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<style scoped>
/* 모든 요소에 대한 box-sizing 설정 */
*,
*::before,
*::after {
  box-sizing: border-box; /* 모든 요소의 너비 계산을 border-box로 설정 */
}

/* html, body, #app 요소에 높이 설정 추가 */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  overflow: auto; /* 스크롤 가능하도록 설정 */
  overflow-x: auto; /* 하단 스크롤 가능하도록 설정 */
}

.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%; /* 전체 너비를 차지하도록 설정 */
  overflow-x: auto; /* 하단 스크롤 가능하도록 설정 */
}

.container {
  flex: 1;
  width: 100%; /* 전체 너비를 차지하도록 설정 */
  max-width: 1200px; /* 최대 너비를 설정해서 콘텐츠가 지나치게 넓어지지 않도록 */
  margin: 0 auto;
  padding: 20px; /* 여백 추가 */
  box-sizing: border-box; /* padding과 border를 포함해서 너비를 계산 */
  overflow-x: auto; /* 하단 스크롤 가능하도록 설정 */
}

/* 기본적인 body 설정 */
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

footer {
  width: 100%;
  text-align: center;
  background: #f1f1f1;
  padding: 10px;
}
</style>
