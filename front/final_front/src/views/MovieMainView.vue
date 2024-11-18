<template>
<h1>영화 메인</h1>
</template>

<script setup>
import MovieMain from '@/components/movie/MovieMain.vue';
import { useMovieStore } from '@/stores/counter';
import { onMounted } from 'vue';

const movies = useMovieStore()
onMounted(() => {
  movies.getMovies()
})
</script>

<style scoped>

</style>