<template>
  <div>
    <div class="movie-container" v-if="recommendedMovies.length > 0">
      <h2>{{ props.userData.username }}님이 추천 받은 영화</h2>
      <div
        class="movie-card"
        v-for="movie in recommendedMovies"
        :key="movie.id"
      >
        <img
          v-if="movie.poster_path"
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          :alt="movie.title"
          class="movie-poster"
          @click="goDetail(movie.id)"
        />
        <h4 class="movie-title">{{ movie.title }}</h4>
        <p class="movie-overview">{{ movie.overview }}</p>
        <div class="rating">
          <span v-for="star in 5" :key="star" :class="{'filled-star': star <= movie.vote_average / 2, 'empty-star': star > movie.vote_average / 2}">
            {{ star <= movie.vote_average / 2 ? '⭐' : '☆' }}
          </span>
        </div>
      </div>
    </div>
    <p v-else>추천된 영화가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
const router = useRouter()
const props = defineProps({
  userData: Object,
});

const recommendedMovies = ref([]);

const goDetail = (id) =>{
  router.push({name:'detail', params : {movie_id:id}})
}
// 영화 정보를 가져오는 함수
const fetchMovieDetails = async (movieId) => {
  try {
    const apiKey = '5fd7a43ce2aa11c0b6d86d8111209b54'; // TMDB API 키
    const response = await axios.get(
      `https://api.themoviedb.org/3/movie/${movieId}?api_key=${apiKey}&language=ko-KR`
    );
    return response.data;
  } catch (error) {
    console.error('영화 정보 가져오기 오류:', error);
  }
};

// 추천 받은 영화 ID로 영화 정보 들고 오는 함수
const fetchRecommendedMovies = async () => {
  if (props.userData?.recommend_movie?.[0]?.recommend_movie) {
    const movieIds = props.userData.recommend_movie[0].recommend_movie;

    if (Array.isArray(movieIds)) {
      for (const movieId of movieIds) {
        const movieData = await fetchMovieDetails(movieId);
        if (movieData) {
          recommendedMovies.value.push(movieData);
        }
      }
    } else {
      console.warn('추천 영화 목록이 비어 있거나 형식이 잘못되었습니다.');
    }
  } else {
    console.warn('recommend_movie 데이터가 없습니다.');
  }
};

// 컴포넌트가 마운트될 때 추천 영화 정보 가져오기
onMounted(() => {
  // 데이터가 존재하는지 확인 후 fetchRecommendedMovies 호출
  if (props.userData && Object.keys(props.userData).length !== 0) {
    fetchRecommendedMovies();
  } else {
    console.warn('userData가 비어있습니다.');
  }
});
</script>

<style scoped>
.movie-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
  padding-top: 40px;
}

.movie-card {
  background: #fff;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 10px;
  margin-bottom: 15px;
}

.movie-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.movie-overview {
  font-size: 1rem;
  margin-bottom: 10px;
  color: #555;
  line-height: 1.6;
}

.rating {
  margin-top: 10px;
}

.filled-star {
  color: #f1c40f;
  font-size: 1.5rem;
}

.empty-star {
  color: #bdc3c7;
  font-size: 1.5rem;
}
</style>
