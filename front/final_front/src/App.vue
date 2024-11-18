<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Footer from './components/common/Footer.vue';
Footer
</script>

<template>
<div class="container">
  <nav>
    <RouterLink to="/main">MovieMain</RouterLink>
  </nav>
  <RouterView />
</div>
  <Footer/>
</template>

<style scoped>
.container {
  margin: 0 auto;
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}


</style>