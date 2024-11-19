<template>
  <div class="mypage-container">
    <div class="top">
      <div class="mydata-container">
        <MyData :userData="userData" />
      </div>
      <div class="calendar-container">
        <Calendar />
      </div>
    </div>
  </div>
</template>

<script setup>
import MyData from '@/components/mypage/MyData.vue';
import { useMovieStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import Calendar from '@/components/mypage/Calendar.vue';

const store = useMovieStore();
const route = useRoute();
const userData = ref({});

onMounted(async () => {
  const userId = route.params.user_id;

  if (store.token) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/user/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(res => {
        console.log('유저 데이터:', res.data);
        userData.value = res.data; // 유저 데이터 저장
      })
      .catch(err => {
        console.log('마이페이지 정보를 불러오는 중 오류:', err);
      });
  } else {
    console.error('토큰이 없습니다. 로그인 후 다시 시도해주세요.');
  }
});
</script>

<style scoped>
.mypage-container {
  max-width: 1200px; /* 페이지 전체 너비를 설정 */
  width: 95%; /* 페이지 전체를 꽉 채우기 위해 비율 조정 */
  margin: 0 auto; /* 화면 중앙 정렬 */
  padding: 20px;
  }

.top {
  display: flex;
  gap: 20px;
  height: 400px;
}
.mydata-container {
  flex: 3.5; /* MyData의 비율 */
}

.calendar-container {
  flex: 6.5; /* Calendar의 비율 */
}
</style>
