<template>
  <div class="ranking-container">
    <p class="ranking-title">조약돌 랭킹</p>
    <div class="user-container">
      <div v-for="(user, index) in topUsers" :key="index" class="user">
        <div class="one-user">
          <div
            class="rank-icon"
            :class="{ first: index === 0, second: index === 1, third: index === 2 }"
          >
            {{ index + 1 }}
          </div>
          <p class="username">{{ user.username }}</p>
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
.one-user {
  display: flex;
  width: 100%;
}
.ranking-container {
  max-width: 500px; /* 컨테이너 너비 축소 */
  margin: 0 auto;
  padding: 10px; /* 내부 패딩 축소 */
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1); /* 그림자 약간 축소 */
}

.ranking-title {
  text-align: center;
  font-size: 1.2rem; /* 제목 크기 축소 */
  font-weight: bold;
  color: #444;
  margin: 0;
  margin-bottom: 10px;
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
</style>
