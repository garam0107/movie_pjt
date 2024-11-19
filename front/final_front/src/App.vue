<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Footer from './components/common/Footer.vue';
import Header from './components/common/Header.vue';
</script>

<template>
  <Header />
    <div class="layout-container">
        <main class="container">
            <router-view />
        </main>
        <Footer />
    </div>
</template>s

<style scoped>
.layout-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.container {
    flex: 1;
    margin: 0 auto;
    padding: 20px;
    /* box-sizing: border-box; */
}

body {
    margin: 0;
    padding: 0;
    /* box-sizing: border-box; */
    font-family: Arial, sans-serif;
}

</style>