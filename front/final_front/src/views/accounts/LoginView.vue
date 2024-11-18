<template>
    <div>
        <h1>Login Page</h1>
        <form @submit.prevent="login">
            <label for="username">id:</label>
            <input type="text" id="username" v-model.trim="username">
            <br>
            <label for="password">password : </label>
            <input type="password" id="password" v-model.trim="password">
            <input type="submit" value="login">
        </form>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref } from 'vue';
const username = ref(null)
const password = ref(null)
const store = useMovieStore()
const login = function() {
    const payload = {
        username: username.value,
        password: password.value
    }
    store.login(payload)
}
</script>

<style lang="scss" scoped>

</style>