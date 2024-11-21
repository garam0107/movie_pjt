<template>
  <div class="mypage-container">
    <div class="top">
      <div class="mydata-container">
        <MyData :userData="userData" />
      </div>
      <div class="calendar-container">
        <Calendar :userData="userData"/>
      </div>
    </div>
    <div class="bottom">
      <div class="my-movie">
        <MyMovie/>
      </div>
      <div class="my-comment">
        <MyComment/>
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
import MyMovie from '@/components/mypage/MyMovie.vue';
import MyComment from '@/components/mypage/MyComment.vue';
const store = useMovieStore();
const route = useRoute();
const userData = ref({});

onMounted(async () => {
  const userId = route.params.user_id; // URL에서 user_id를 가져옴

  if (store.token) {
    // 특정 유저의 데이터를 불러오기 위해 userId 사용
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId}/mypage/`, // 특정 사용자 데이터 요청
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
  width: 100%; /* 페이지 전체를 꽉 채우기 위해 비율 조정 */
  margin: 0 auto; /* 화면 중앙 정렬 */
  padding: 20px;
  }

.top {
  display: flex;
  gap: 20px;
  height: 400px;
}
.mydata-container {
  flex: 3.5;
}

.calendar-container {
  flex: 6.5; 
}

.bottom {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.my-movie {
  flex: 3.5;
}
.my-comment {
  flex: 6.5;
}
</style>
