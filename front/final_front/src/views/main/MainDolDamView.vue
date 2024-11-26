<template>
  <WhatisDolDam/>
  <div v-if="userId" class="only-user">
    <div class="follow">
      <FollowComment :userId="userId"/>
    </div>
    <div class="top">
      <TopUser/>
    </div>
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
  gap: 20px;
  align-items: stretch;
}

.follow {
  flex: 8;
}
.top {
  flex: 2;
}
</style>