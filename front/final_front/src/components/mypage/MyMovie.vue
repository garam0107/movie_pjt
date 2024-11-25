<template>
  <div>
    <div class="movie-container" v-if="recommendedMovies.length > 0">
      <h2 class="movie-header">{{ props.userData.nickname }}님이 추천 받은 마지막 영화🎦</h2>
      <div class="movie-cards">
        <div
          class="movie-card"
          v-for="(movie,index) in recommendedMovies"
          :key="movie.id"
        >
          <img
            v-if="movie.poster_path"
            :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
            :alt="movie.title"
            class="movie-poster"
            @click="goDetail(movie.id)"
          />
        
          
          <div 
          class="movie-reason"
          v-if="recommendedReasons[index]"
          >
            <p>{{recommendedReasons[index]}}</p>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="no-mymovie">추천된 영화가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, defineProps, watch, onMounted, toRaw} from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  userData: Object
})

const recommendedMovies = ref([])
const recommendedReasons = ref([])
const goDetail = (id) => {
  router.push({ name: 'detail', params: { movie_id: id } })
}

// 영화 정보를 가져오는 함수
const fetchMovieDetails = async (movieId) => {
  try {
    const apiKey = '5fd7a43ce2aa11c0b6d86d8111209b54' // TMDB API 키
    const response = await axios.get(
      `https://api.themoviedb.org/3/movie/${movieId}?api_key=${apiKey}&language=ko-KR`
    )
    return response.data
  } catch (error) {
    console.error('영화 정보 가져오기 오류:', error)
    return null
  }
}

// 추천 받은 영화 ID로 영화 정보를 들고 오는 함수
const fetchRecommendedMovies = async () => {
  recommendedMovies.value = [] // 이전 추천 초기화
  

  if (
    props.userData?.recommend_movie &&
    Array.isArray(props.userData.recommend_movie) &&
    props.userData.recommend_movie.length > 0
  ) {
    const lastRecommendationSet =
      props.userData.recommend_movie[props.userData.recommend_movie.length - 1]
    if (
      lastRecommendationSet?.recommend_movie &&
      Array.isArray(lastRecommendationSet.recommend_movie) &&
      lastRecommendationSet.recommend_movie.length > 0
    ) {
      // 두 개의 영화 ID 가져오기
      for (const movieId of lastRecommendationSet.recommend_movie) {
        const movieData = await fetchMovieDetails(movieId)
        if (movieData) {
          recommendedMovies.value.push(movieData)
        }
      }
    } else {
      console.warn('추천 영화 목록이 비어 있거나 형식이 잘못되었습니다.')
    }
  } else {
    console.warn('recommend_movie 데이터가 없습니다.')
  }
}
const fetchRecommendedReasons = async () => {
  // recommendedReasons 초기화
  recommendedReasons.value = [];
  
  // recommend_reasons가 배열인지 확인하고, 마지막 요소 가져오기
  if (
    props.userData?.recommend_reasons &&
    Array.isArray(props.userData.recommend_reasons) &&
    props.userData.recommend_reasons.length > 0
  ) {
    // 마지막 recommend_reasons 객체 가져오기
    const lastRecommendationReasonsSet =
      props.userData.recommend_reasons[props.userData.recommend_reasons.length - 1];

    // 마지막 요소 안의 recommend_reasons 객체 가져오기
    const reasons = lastRecommendationReasonsSet?.recommend_reasons;

    if (reasons) {
      // 두 개의 리뷰 접근
      const review1 = reasons?.today_diary_review1;
      const review2 = reasons?.today_diary_review2;

      // 리뷰가 존재하는지 확인하고 배열에 추가
      if (review1) {
        recommendedReasons.value.push(review1);
      }
      if (review2) {
        recommendedReasons.value.push(review2);
      }

      // 리뷰 출력 (혹은 필요한 작업 수행)
      if (recommendedReasons.value.length > 0) {
        console.log('추천 리뷰 목록:', recommendedReasons.value);
      } else {
        console.warn('추천 리뷰 목록이 비어 있거나 형식이 잘못되었습니다.');
      }
    } else {
      console.warn('추천 이유 데이터가 없습니다.');
    }
  } else {
    console.warn('recommend_movie 데이터가 없습니다.');
  }
}


// userData 변경 감지 시 추천 영화 정보 가져오기
watch(
  () => props.userData,
  (newValue) => {
    if (newValue && Object.keys(newValue).length !== 0) {
      fetchRecommendedMovies()
      fetchRecommendedReasons()
    }
  },
  { immediate: true, deep: true }
)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
/* .movie-container {
  padding-top: 20px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
} */

.movie-header {
  font-size: 1.3rem;
  color: #34495e;
  margin-bottom: 20px;
  text-align: center;
  font-family: "Noto Sans KR", sans-serif;
  letter-spacing: 0.05em;
}

.movie-cards {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 10px;
}

.movie-card {
  background: #ffffff;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.4);
  width: 40%;
  transition: transform 0.3s ease;
  cursor: pointer;
  position: relative;
  border: 1px solid #d1d1d1;
  font-family: 'Roboto', sans-serif;
}

.movie-card:hover {
  transform: translateY(-3px);
}

.movie-poster {
  width: 100%;
  height: 221px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 8px;
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
}


.movie-reason {
  font-size: 0.9rem;
  color: #7a7a7a;
  font-style: italic;
  line-height: 1.4;
  margin-bottom: 10px;
  text-align: center;
}

.movie-card::before {
  content: "추천";
  font-size: 1rem;
  color: #e63946;
  position: absolute;
  top: -10px;
  left: 1px;
  background: #fffcf2;
  padding: 3px 6px;
  border-radius: 8px;
  border: 1px solid #e63946;
  font-family: "Jua", sans-serif;
}

.no-mymovie {
  font-family: "Noto Sans KR", sans-serif;
}

</style>
