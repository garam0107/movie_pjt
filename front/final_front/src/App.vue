<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Footer from '@/components/movie/common/Footer.vue';
Footer
</script>

<template>

      <nav>
        <RouterLink to="/main">MovieMain</RouterLink>
      </nav>

  <RouterView />
  <Footer/>
</template>

<style scoped>

</style>
