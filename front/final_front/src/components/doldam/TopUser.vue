<template>
  <div class="ranking-container">
    <p class="ranking-title">Top User 👑</p>
    <div class="user-container">
      <div v-for="(user, index) in topUsers" :key="index" class="user">
        <div class="one-user">
          <div
            class="rank-icon"
            :class="{ first: index === 0, second: index === 1, third: index === 2 }"
          >
            {{ index + 1 }}
          </div>
          <RouterLink :to="`/mypage/${user.username}/`" class="movie-link">
            <p class="username">{{ user.nickname }}</p>
          </RouterLink>
          <div class="stone-display">
            <img src="@/assets/stone_icon.png" alt="stone icon" class="stone-icon" />
            <span>{{ user.stone }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { onMounted, ref } from 'vue';
const store = useMovieStore()
const topUsers = ref([])
onMounted(() => {
  if (store.token) {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/accounts/all',
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })
    .then((res) => {
      console.log('랭킹 : ', res)
      topUsers.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }
})

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Parkinsans:wght@300..800&display=swap');
.one-user {
  display: flex;
  width: 100%;
}
.ranking-container {
  position: relative; /* ::before의 기준 */
  max-width: 500px; /* 컨테이너 너비 */
  margin: 0 auto;
  padding: 10px; /* 내부 패딩 */
  border-radius: 10px; /* 테두리 둥글게 */
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1); /* 그림자 */
  background-color: transparent; /* 투명 배경 */
  z-index: 1; /* 내용 위에 배경 레이어 설정 */
}

.ranking-container::before {
  content: ''; /* 가상 요소 */
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle, rgba(255, 255, 255, 0.5) 50%, rgba(255, 255, 255, 0.8) 90%, rgba(255, 255, 255, 1) 100%), 
    url('@/assets/stone_back.png'); /* 배경 이미지 경로 */
  background-size: cover; /* 배경 이미지 크기 조정 */
  background-position: center; /* 배경 이미지 위치 */
  background-repeat: no-repeat; /* 이미지 반복 방지 */
  opacity: 0.95; /* 배경 투명도 조정 */
  border-radius: 10px; /* 부모와 동일한 테두리 */
  z-index: -1; /* 컨텐츠 뒤로 배치 */
}

.ranking-title {
  font-family: "Parkinsans", sans-serif;
  text-align: center;
  font-size: 1.2rem; 
  font-weight: bold;
  color: black;
  margin: 0;
}

.user-container {
  display: flex;
  flex-direction: column;
  gap: 8px; /* 카드 간격 축소 */
}

.user {
  display: flex;
  align-items: center;
  padding: 6px 8px; /* 카드 내부 패딩 축소 */
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 그림자 축소 */
}

.one-user {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.rank-icon {
  font-family: "Parkinsans", sans-serif;
  font-size: 1rem; /* 순위 아이콘 크기 축소 */
  font-weight: bold;
  width: 25px;
  height: 25px; /* 아이콘 크기 축소 */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ddd;
  color: white;
  margin-right: 8px; /* 간격 축소 */
}

/* 1등, 2등, 3등 스타일 */
.rank-icon.first {
  background: gold;
  color: black;
  font-size: 1.2rem; /* 크기 약간 축소 */
  box-shadow: 0 0 3px gold; /* 그림자 축소 */
}

.rank-icon.second {
  background: silver;
  color: black;
  font-size: 1.1rem;
  box-shadow: 0 0 3px silver;
}

.rank-icon.third {
  background: #cd7f32; /* 청동색 */
  color: black;
  font-size: 1rem;
  box-shadow: 0 0 3px #cd7f32;
}

.username {
  font-size: 0.9rem; /* 이름 크기 축소 */
  font-weight: bold;
  color: #333;
  font-family: "Noto Sans KR", sans-serif;
}

.stone-display {
  display: flex;
  align-items: center;
  gap: 4px; /* 간격 축소 */
}

.stone-icon {
  width: 40px; /* 아이콘 크기 축소 */
  height: 40px;
}

.stone-display span {
  font-size: 0.9rem; /* 글자 크기 축소 */
  font-weight: bold;
  color: #555;
}

.movie-link {
  text-decoration: none;
}
</style>
