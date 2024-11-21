<template>
  <div>
    <div class="top-movie-container">
      <p class="h2tag">Weekly HOT 랭킹</p>
      <div class="wrapper" v-if="weelyMovies.length > 0">
        <div v-for="(movie, index) in weelyMovies" :key="movie.id" class="movie-item">
          <div class="rank">{{ index + 1 }}</div>
          <RouterLink :to="`/movie/${movie.id}`" class="movie-link">
            <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" alt="poster" class="poster_img">
            <div class="movie-info">
              <p class="movie_title">{{ movie.title }}</p>
              <p class="movie-details">
                평점:  {{ movie.vote_average.toFixed(1) }} ★
              </p>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { onMounted, watch, ref } from 'vue';
const store = useMovieStore()
const weelyMovies = ref([])
const movies = ref([])
onMounted(async() => {
  await store.getMovies()
  movies.value = store.movies
  weelyMovies.value = [...movies.value]
    .sort((a, b) => b.vote_average - a.vote_average)
    .slice(0, 10)
})

watch(() => store.movies, (newMovies) => {
  movies.value = newMovies
  weelyMovies.value = [...newMovies]
    .sort((a, b) => b.vote_average - a.vote_average)
    .slice(0, 10)
})
</script>

<style scoped>
.top-movie-container {
  padding: 5px;
}

.top-movie-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.wrapper {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 20px;
}

.movie-item {
  position: relative;
  transition: transform 0.3s ease;
}

.movie-item:hover {
  transform: scale(1.05);
}

.rank {
  position: absolute;
  top: 5px;
  left: 5px;
  color: white;
  border-radius: 10%;
  width: 15px;
  height: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.poster_img {
  width: 100%;
  max-width: 200px;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.movie-link {
  text-decoration: none;
}

.movie-info {
  margin-top: 10px;
  text-align: left;
  font-size: 0.9rem;
  color: #333;
}

.movie_title {
  margin-bottom: 5px;
  font-size: 0.7rem;
}

.movie-details {
  font-size: 0.8rem;
  color: #777;
  margin-top: 0;
}
</style>