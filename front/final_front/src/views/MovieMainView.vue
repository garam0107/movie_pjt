<template>
<div class="container">
  <h1>영화 메인</h1>
  <div>
    트레일러 하나 보이자
  </div>
  <div>
    <TopMovieComponent/>
  </div>
</div>
</template>

<script setup>
import TopMovieComponent from '@/components/movie/TopMovieComponent.vue';



</script>

<style scoped>
.container{ 
  width: 70%;
}
</style>