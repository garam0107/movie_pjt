<template>
  <WhatisDolDam/>
  <div v-if="userId" class="only-user">
    <FollowComment :userId="userId"/>
    <TopUser/>
  </div>
  <WeeklyMovie/>
</template>

<script setup>
import FollowComment from '@/components/doldam/FollowComment.vue';
import TopUser from '@/components/doldam/TopUser.vue';
import WeeklyMovie from '@/components/doldam/WeeklyMovie.vue';
import WhatisDolDam from '@/components/doldam/WhatisDolDam.vue';
import { useMovieStore } from '@/stores/counter';
import { computed } from 'vue';
const store = useMovieStore()
const userId = computed(() => store.userId)
</script>
 
<style scope>
.only-user {
  display: flex;
  gap: 100px;
}
</style>