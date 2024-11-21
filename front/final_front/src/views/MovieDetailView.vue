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
      <div class="backdrop-info2">
        <p v-if="store.token" class="likecountnumber">좋아요 수 : {{ likeCount }}</p>
        <button @click="toggleLike" class="like-button">
          {{ isLiked ? '❤️' : '🤍' }}
        </button>
        <button @click="openReviewModal" class="action-button">📝</button>
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
      <p>Actors</p>
      <div class="actors">
        <div v-for="actor in store.detailMovie.actors.slice(0, 10)" :key="actor.id" class="actor">
          <img :src="`https://image.tmdb.org/t/p/w500/${actor.poster_path}`" alt="actor" class="actor-poster">
          <p class="actor_name">{{ actor.name }}</p>
        </div>
      </div>
    </div>
    <div v-else>x
      <p>배우 정보가 없습니다.</p>
    </div>
    <div>
      <MovieCommentComponent/>
    </div>


    <!-- 리뷰 작성 모달 -->
    <div v-if="showReviewModal" class="modal">
      <div class="modal-content">
        <h3>리뷰 작성</h3>
        <input type="text" v-model="reviewTitle" placeholder="제목" class="input-field"/>
        <textarea v-model="reviewContent" placeholder="내용" class="textarea-field"></textarea>
        <div class="rating-selection">
          <p>별점 선택</p>
          <div class="stars">
            <span 
              v-for="star in 5" 
              :key="star" 
              :class="['star', {'selected': star <= selectedRating, 'hovered': star <= hoveredRating}]" 
              @click="selectedRating = star"
              @mouseover="hoveredRating = star"
              @mouseleave="hoveredRating = 0"
            >★</span>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="submitReview" class="save-button">저장</button>
          <button @click="showReviewModal = false" class="close-button">닫기</button>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>

import MovieCommentComponent from '@/components/movie/MovieCommentComponent.vue';
import router from '@/router';
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const store = useMovieStore();
const route = useRoute();
const isLiked = ref(false)
const likeCount = ref(0)
const movieId = route.params.movie_id

// 모달창.. 
const showReviewModal = ref(false);
const reviewTitle = ref('');
const reviewContent = ref('');
const selectedRating = ref(0);
const hoveredRating = ref(0);

onMounted(async () => {
  await store.getDetailMovie(movieId);
  if(store.token) {
    axios ({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/detail/${movieId}/like/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })
    .then((res) => {
      console.log(res)
      isLiked.value = res.data.liked
      likeCount.value = res.data.like_count
    })
    .catch((err) => {
      console.log(err)
    })
  }
});
const toggleLike = () => {
  if(!store.token){
    alert('로그인이 필요합니다.')
    router.push({ name: 'LoginView' })
  }
  const requestUrl = `http://127.0.0.1:8000/movies/detail/${movieId}/like/`
  console.log('Request URL:', requestUrl)
  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/movies/detail/${movieId}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log(res)
      isLiked.value = res.data.liked
      likeCount.value = res.data.like_count
    })
    .catch((err) => {
      console.log(err)
    })

}

// 모달 열기
const openReviewModal = () => {
  showReviewModal.value = true;
};

// 리뷰 제출
const submitReview = () => {
  if (!reviewTitle.value || !reviewContent.value || selectedRating.value === 0) {
    alert('제목, 내용, 별점을 모두 입력해주세요.')
    return
  }

  axios.post(`http://127.0.0.1:8000/movies/detail/${movieId}/create_review/`, {
    title: reviewTitle.value,
    content: reviewContent.value,
    rating: selectedRating.value
  }, {
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((res) => {
    console.log('리뷰 저장 성공:', res.data)
    showReviewModal.value = false
    reviewTitle.value = ''
    reviewContent.value = ''
    selectedRating.value = 0
    alert('리뷰가 성공적으로 작성되었습니다!')
    location.reload()
  })
  .catch((err) => {
    console.error('리뷰 저장 실패:', err)
  })
}



</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Hahmlet:wght@100..900&family=Noto+Sans+KR:wght@100..900&family=Noto+Serif+KR:wght@200..900&display=swap');
.likecountnumber {
  font-size: 15px;
  font-family: "Noto Sans KR", sans-serif;
}

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
  top: 240px;
  left: 30px;
  color: #fff;
}

.backdrop-info2 {
  position: absolute;
  top: 380px;
  right: 18px;
  color: #fff;
  display: flex;
  gap: 10px; /* 버튼 간격 추가 */
}
.action-button {
  /* padding: 10px 20px; */
  border: none;
  /* background-color: #ff007f;  */
  color: #ffffff; 
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 8px; 
  cursor: pointer;
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
.actors:hover {
  transform: translateY(-5px);
}
.actors {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.actor {
  text-align: center;
}
.actor_name {
  font-size: 12px;
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
  flex-direction: column;
  align-items: center;
}

.stars span {
  font-size: 1.8rem;
  color: lightgray;
  cursor: pointer;
  transition: color 0.3s ease, transform 0.2s;
}

.stars span.hovered,
.stars span.selected {
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

.like-button {
  font-size: 2rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease;
  color: #ff007f;
}

.like-button:hover {
  transform: scale(1.1);
}

/* 모달 스타일링 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #ffffff;
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
}

.input-field, .textarea-field {
  width: 80%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.input-field:focus, .textarea-field:focus {
  border-color: #ff007f;
  outline: none;
}

.stars {
  display: flex;
  gap: 5px;
}

.star {
  font-size: 2rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.star.selected,
.star.hovered {
  color: gold;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.save-button, .close-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.2s;
}

.save-button {
  background-color: gray;
  color: #ffffff;
}

.close-button {
  background-color: #ccc;
  color: #333;
}

.save-button:hover {
  background-color: #555;
  transform: translateY(-2px);
}

.close-button:hover {
  background-color: #aaa;
  transform: translateY(-2px);
}

.review-button {
  background-color: #ff007f;
  color: #ffffff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s;
}

.review-button:hover {
  background-color: #e00070;
  transform: translateY(-2px);
}
</style>
