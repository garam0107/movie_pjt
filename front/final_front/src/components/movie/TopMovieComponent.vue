<template>
    <div class="top-movie-container">
      <p class="h2tag">돌담뮤비디아 HOT 랭킹</p>
      <div class="wrapper" v-if="topMovies.length > 0">
        <div v-for="(movie, index) in topMovies" :key="movie.id" class="movie-item">
          <div class="rank">{{ index + 1 }}</div>
          <RouterLink :to="`/movie/${movie.id}`" class="movie-link">
            <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" alt="poster" class="poster_img">
            <div class="movie-info">
              <p class="movie_title">{{ movie.title }}</p>
              <p class="movie-details">
                {{ movie.release_date.slice(0, 4) }} •  {{ movie.production_country || '정보 없음' }}<br>
                평점:  {{ movie.vote_average.toFixed(1) }} ★
              </p>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
    <div class="top-movie-container">
      <p class="h2tag">사용자가 뽑은 최고의 영화</p>
      <div class="wrapper" v-if="topMovies.length > 0">
        <div v-for="(movie, index) in voteMovies" :key="movie.id" class="movie-item">
          <div class="rank">{{ index + 1 }}</div>
          <RouterLink :to="`/movie/${movie.id}`" class="movie-link">
            <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" alt="poster" class="poster_img">
            <div class="movie-info">
              <p class="movie_title">{{ movie.title }}</p>
              <p class="movie-details">
                {{ movie.release_date.slice(0, 4) }} •  {{ movie.production_country || '정보 없음' }}<br>
                평점:  {{ movie.vote_average.toFixed(1) }} ★
              </p>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useMovieStore } from '@/stores/counter';

const movies = ref([]);
const topMovies = ref([]);
const store = useMovieStore();
const voteMovies = ref([])
onMounted(async () => {
  await store.getMovies()
  movies.value = store.movies

  topMovies.value = [...movies.value]
    .sort((a, b) => b.popularity - a.popularity)
    .slice(0, 10)

  voteMovies.value = [...movies.value]
    .sort((a, b) => b.vote_count - a.vote_count)
    .slice(0, 10)
  console.log(voteMovies)
});

watch(() => store.movies, (newMovies) => {
  movies.value = newMovies
  
  topMovies.value = [...newMovies]
    .sort((a, b) => b.popularity - a.popularity)
    .slice(0, 10)

    voteMovies.value = [...movies.value]
    .sort((a, b) => b.vote_count - a.vote_count)
    .slice(0, 10)
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Hahmlet:wght@100..900&family=Noto+Sans+KR:wght@100..900&family=Noto+Serif+KR:wght@200..900&display=swap');
.h2tag {
  font-family: "Noto Sans KR", sans-serif;
  font-weight: 800; 
  font-size: large;
  font-style: normal;
}

.top-movie-container {
  padding: 5px;
  /* margin: 0 auto; */
}

.top-movie-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.wrapper {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
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
  background: gray;
  color: white;
  border-radius: 10%;
  width: 30px;
  height: 30px;
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
  font-weight: bold;
  margin-bottom: 5px;
}

.movie-details {
  font-size: 0.8rem;
  color: #777;
}
</style>
