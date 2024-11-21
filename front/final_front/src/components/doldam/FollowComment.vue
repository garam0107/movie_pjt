<template>
  <div>
    <h2>대충 내 이웃이 쓴 코멘트 </h2>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';
const store = useMovieStore()
const comments = ref([])
const token = store.token
const userId = defineProps ({
  userId: String
})
const userData = ref([])
// console.log(token)
console.log(userId.userId)
onMounted(() => {
  if (store.token) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId.userId}/mypage/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      userData.value = res.data;
    })
    .catch((err) => {
      console.error('유저 정보를 불러오는 중 오류 발생:', err);
    });

    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId.userId}/follow/`,
      headers: {
          Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      console.log(res)
      comments.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }
})

</script>

<style>
</style>