<template>
  <div class="mypage-container" v-if="userDataLoaded">
    <div class="top">
      <div class="mydata-container">
        <MyData :userData="userData" />
      </div>
      <div class="calendar-container">
        <Calendar :userData="userData" :key="userData.id"/>
      </div>
    </div>
    <div class="bottom">
      <div class="my-movie">
        <MyMovie :userData="userData"/>
      </div>
      <div class="my-comment">
        <MyComment :userData="userData"/>
      </div>
    </div>
  </div>
  <div v-else>
    <p>로딩 중...</p> <!-- 데이터 로딩 중임을 나타내는 표시 -->
  </div>
</template>

<script setup>
import MyData from '@/components/mypage/MyData.vue';
import { useMovieStore } from '@/stores/counter';
import { onMounted, ref, onUpdated} from 'vue';
import axios from 'axios';
import { onBeforeRouteUpdate, useRoute,useRouter } from 'vue-router';
import Calendar from '@/components/mypage/Calendar.vue';
import MyMovie from '@/components/mypage/MyMovie.vue';
import MyComment from '@/components/mypage/MyComment.vue';

const store = useMovieStore();
const route = useRoute();
const router = useRouter()
const userData = ref({});
const userDataLoaded = ref(false); // 로딩 상태 추적



// 유저 데이터를 가져오는 함수
const fetchUserData = (userId) => {
  if (store.token) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId}/mypage/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })
      .then((res) => {
        console.log('유저 데이터:', res.data);
        userData.value = res.data;
        userDataLoaded.value = true; // 데이터 로드 완료 시 true로 변경
      })
      .catch((err) => {
        console.log('마이페이지 정보를 불러오는 중 오류:', err);
        userDataLoaded.value = false; // 오류 발생 시 로드 완료 false
      });
  } else {
    console.error('토큰이 없습니다. 로그인 후 다시 시도해주세요.');
    userDataLoaded.value = false; // 토큰이 없을 때도 로딩 표시
  }
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  const userId = route.params.user_id; // URL에서 user_id 가져오기
  fetchUserData(userId); // 초기 데이터 로드
});

// 라우트 변경 시 데이터 갱신
onBeforeRouteUpdate((to) => {
  const newUserId = to.params.user_id; // 새 라우트의 user_id 가져오기
  fetchUserData(newUserId); // 새 데이터 로드
  
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
