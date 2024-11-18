<template>
  <div class="container noto-sans-kr-container">
    <div class="backdrop-container">
      <img :src="`https://image.tmdb.org/t/p/w500/${store.detailMovie.backdrop_path}`" alt="backdrop" class="backdrop">
      <div class="backdrop-info noto-sans-kr-backdrop-info">
        <h2>{{ store.detailMovie.title }}</h2>
        <p>장르: {{ store.detailMovie.genres?.map(genre => genre.name).join(', ') }}</p>
        <p>개봉일: {{ store.detailMovie.release_date }}</p>
        <p>국가: {{ store.detailMovie.production_country || '정보 없음' }}</p>
      </div>
    </div>
    <div class="movie-detail">
      <img :src="`https://image.tmdb.org/t/p/w500/${store.detailMovie.poster_path}`" alt="poster" class="poster">
      <div class="movie-info noto-sans-kr-movie-info">
        <p>평균 평점: {{ store.detailMovie.vote_average }}</p>
        <p>감독: {{ store.detailMovie.director }}</p>
        <p>상영 시간: {{ store.detailMovie.runtime }}분</p>
        <p>{{ store.detailMovie.overview }}</p>
      </div>
    </div>
    <div v-if="store.detailMovie.actors && store.detailMovie.actors.length > 0">
      <p>배우</p>
      <div class="actors">
        <div v-for="actor in store.detailMovie.actors.slice(0, 10)" :key="actor.id" class="actor">
          <img :src="`https://image.tmdb.org/t/p/w500/${actor.poster_path}`" alt="actor" class="actor-poster">
          <p>{{ actor.name }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>배우 정보가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';

const store = useMovieStore();
const route = useRoute();

onMounted(async () => {
  const movieId = route.params.movie_id;
  await store.getDetailMovie(movieId);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Hahmlet:wght@100..900&family=Noto+Sans+KR:wght@100..900&family=Noto+Serif+KR:wght@200..900&display=swap');

.noto-sans-kr-container {
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
}

.noto-sans-kr-backdrop-info {
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: 600;
  font-style: normal;
}

.noto-sans-kr-movie-info {
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
}

.container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
}

.backdrop-container {
  position: relative;
  margin-bottom: 30px;
}

.backdrop {
  width: 100%;
  height: 450px;
  object-fit: cover;
  filter: brightness(70%);
  border-radius: 10px;
}

.backdrop-info {
  position: absolute;
  top: 250px;
  left: 30px;
  color: #fff;
}

.backdrop-info h2 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-family: 'Hahmlet', serif;
}

.backdrop-info p {
  font-size: 1.2rem;
  margin: 5px 0;
}

.movie-detail {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 30px;
}

.poster {
  width: 15%;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.movie-info {
  width: 70%;
  color: #333;
}

.movie-info p {
  font-size: 1.2rem;
  margin: 10px 0;
}

.actors {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.actor {
  text-align: center;
}

.actor-poster {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 10px;
}

.rating-graph {
  margin-top: 30px;
  text-align: center;
}

.graph-placeholder {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.movie-actions {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  justify-content: center;
}

.rating {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stars span {
  font-size: 2rem;
  color: gold;
}

.movie-ad {
  margin-top: 30px;
  text-align: center;
}

.ad-image {
  width: 100%;
  max-width: 500px;
  margin-bottom: 10px;
}
</style>
