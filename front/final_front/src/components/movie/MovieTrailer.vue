<template>
  <div class="trailer-container">
    <div class="trailer-video">
      <iframe
        :src="`https://www.youtube.com/embed/${trailerKey}`"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
    <div class="trailer-info">
      <h2 class="movie-title">{{ movie.title }}</h2>
      <p class="release-date">개봉일: {{ movie.release_date }}</p>
      <p class="overview">{{ movie.overview }}</p>
      <div class="additional-info">
        <span class="genres">장르: {{ movie.genres?.map(genre => genre.name).join(', ') }}</span>
        <span class="rating">평점: ★ {{ movie.vote_average }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const movie = ref({
  title: '청설',
  release_date: '2009-08-28',
  overview:
    '청각 장애를 가진 여동생을 돌보는 양양과, 배달부 톈궈의 순수한 사랑 이야기를 담은 따뜻한 대만 영화입니다.',
  genres: [
    { id: 1, name: '로맨스' },
    { id: 2, name: '드라마' },
  ],
  vote_average: 7.8,
});

const trailerKey = ref('mxE1ct1C7Wg'); 

</script>

<style scoped>
.trailer-container {
  display: flex;
  flex-direction: row;
  gap: 20px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.trailer-video iframe {
  width: 560px;
  height: 315px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.trailer-info {
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.movie-title {
  font-size: 2rem;
  color: #ff007f;
  margin: 0;
}

.release-date {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

.overview {
  font-size: 1rem;
  color: #444;
  line-height: 1.5;
}

.additional-info {
  font-size: 1rem;
  color: #444;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.genres,
.rating {
  font-weight: bold;
}
</style>
