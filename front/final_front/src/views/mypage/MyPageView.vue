<template>
<div>
  <h2>마이페이지</h2>
  <div>
    <MyData/>
    
  </div>
</div>
</template>

<script setup>
import MyData from '@/components/mypage/MyData.vue';
import { useMovieStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
const store = useMovieStore()
const route = useRoute()
const userdata = ref([])
onMounted(async () => {
  const userId = route.params.user_id
  console.log(route.params)
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/accounts/user/',
    headers: {
            Authorization: `Token ${token}`
    }
  })
    .then(res => {
      console.log(res)
    })
    .catch(err => {
      console.log(err)
    })
})

</script>

<style scoped>

</style>