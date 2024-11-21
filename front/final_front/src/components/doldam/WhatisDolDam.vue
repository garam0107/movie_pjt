<template>
  <div class="main-banner">
    <div class="banner-content">
      <img src="@/assets/movie_logo.png" alt="main-logo" class="main-logo" />
      <h4 ref="animatedText"></h4>
      <p>
        일기를 통해 감정을 분석하고, 감정에 기반한 영화와 반대되는 영화를 추천합니다. <br />
        당신의 영화 여정을 지금 시작하세요!
      </p>
      <RouterLink v-if="!userId" :to="{name: 'SignupView'}"><button class="signup-button">회원가입 바로가기</button></RouterLink>
    </div>
  </div>
</template>



<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref, onMounted, computed } from 'vue';
const store = useMovieStore()
const userId = computed(() => store.userId)
const text = "당신의 감정에서 시작되는 특별한 영화 여행"; // 타이핑할 텍스트
const animatedText = ref(null); // h4 요소를 참조

onMounted(() => {
  typeText(animatedText.value, text, 100); // 텍스트를 타이핑 효과로 실행
});

function typeText(element, text, speed) {
  let i = 0;
  function typing() {
    if (i < text.length) {
      element.textContent += text[i];
      i++;
      setTimeout(typing, speed); // 각 글자가 타이핑되는 속도
    }
  }
  typing();
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Hahmlet:wght@100..900&family=Noto+Sans+KR:wght@100..900&family=Noto+Serif+KR:wght@200..900&display=swap');
.main-banner {
  background: radial-gradient(
      circle, 
      rgba(137, 207, 240, 1) 40%, /* 중앙: 선명한 파스텔 블루 */
      rgba(179, 229, 252, 0.7) 70%, /* 중간: 연한 하늘색 */
      rgba(255, 255, 255, 1) 100% /* 가장자리: 완전 흰색 */
    ),
    linear-gradient(
      to bottom,
      rgba(255, 255, 255, 1),
      rgba(255, 255, 255, 0.5) 50%,
      rgba(255, 255, 255, 1)
    ); /* 위아래 방향으로 흰색과 자연스럽게 연결 */
  background-blend-mode: overlay;
  color: #333; /* 텍스트 색상 */
  padding: 10px 10px;
  text-align: center;
  border-radius: 15px;
  margin: 3px auto;
  max-width: 1200px;
}
.banner-content {
  position: relative;
}

.main-logo {
  width: 40%; 
  height: auto;
  margin-bottom: 0px;
  animation: float 3s ease-in-out infinite; 
}

.banner-content h4 {
  font-size: 1.8rem;
  margin-bottom: 15px;
  line-height: 1.5;
  color: black;
  font-family: "Gowun Batang", serif;
  font-weight: 700;
  font-style: normal;
  margin-top: 0;
  position: relative;
  overflow: hidden;
  text-align: center; /* 텍스트를 중앙에 정렬 */
  white-space: nowrap; /* 타이핑 애니메이션에서 텍스트 줄바꿈 방지 */
}

.banner-content h4:hover::after {
  width: 100%;
}

.banner-content p {
  font-size: 1.2rem;
  line-height: 1.8;
  margin: 0 auto;
  max-width: 800px;
  color: black;
  font-family: "Gowun Batang", serif;
  font-weight: 400;
  font-style: normal;
}

.banner-content p:hover {
  transition: all 0.3s ease-in-out;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* 플로팅 애니메이션 */
@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .main-banner {
    padding: 30px 10px;
  }

  .banner-content h1 {
    font-size: 2.5rem;
  }

  .banner-content h2 {
    font-size: 1.5rem;
  }

  .banner-content p {
    font-size: 1rem;
  }

  .main-logo {
    width: 100px;
  }
}

.signup-button {
  padding: 5px 20px;
  font-size: 1rem;
  font-weight: 600;
  color: black;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  margin-top: 7px; 
  font-family: 'Hahmlet', serif;
}

.signup-button:active {
  transform: translateY(0); 
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
</style>
