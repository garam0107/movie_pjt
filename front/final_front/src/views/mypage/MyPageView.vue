<template>
  <div>
    <h2>마이페이지</h2>
    <div>
      <MyData :userData="userData"/>
    </div>
  </div>
</template>

<script setup>
import MyData from '@/components/mypage/MyData.vue';
import { useMovieStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

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

</style>
