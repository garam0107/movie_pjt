<template>
<div>
  <div>
    <!-- <MovieTrailer/> -->
  </div>
  <div>
    <TopMovieComponent/>
  </div>
</div>
</template>

<script setup>
import MovieTrailer from '@/components/movie/MovieTrailer.vue';
import TopMovieComponent from '@/components/movie/TopMovieComponent.vue';
import { useMovieStore } from '@/stores/counter';
import { onMounted } from 'vue';
const store = useMovieStore()
// onMounted(() => {
//   store.checkAuthentication()
// })

</script>

<style scoped>

</style>