<template>
  <div class="comment-section">
    <div class="comment-title">
      <h3>코멘트</h3>
    </div>
    <div v-if="reviews.length === 0" class="no-comments">
      <p>코멘트가 없습니다. 첫 번째 코멘트를 작성해보세요!</p>
    </div>
    <div v-else class="review-grid">
      <div 
        class="review-card" 
        v-for="review in reviews" 
        :key="review.id"
      >
        <h5 class="review-title">{{ review.title }}</h5>
        <p class="review-content">{{ review.content }}</p>
        <div class="rating">
          <span v-for="star in 5" :key="star" :class="{'filled-star': star <= review.rating, 'empty-star': star > review.rating}">
            {{ star <= review.rating ? '⭐' : '☆' }}
          </span>
        </div>
        <p class="review-author">작성자: {{ review.username }}</p>
        <p class="review-date">작성일: {{ formatDate(review.created_at) }}</p>
        <div v-if="review.username === userData.username">
          <button @click="updateComment">리뷰 수정</button>
          <button @click="deleteComment(review.id)">리뷰 삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/counter';
 
const reviews = ref([]);
const route = useRoute();
const movieId = route.params.movie_id;
const userData = ref({});
const store = useMovieStore()

onMounted(() => {
  axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/${movieId}/detail_review/`,
  })
    .then((res) => {
      reviews.value = res.data;
    })
    .catch((err) => {
      console.error(err);
    });
});

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

onMounted(async () => {

  if (store.token) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/user/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(res => {
        console.log('유저 데이터:', res.data);
        userData.value = res.data; 
      })
      .catch(err => {
        console.log('마이페이지 정보를 불러오는 중 오류:', err);
      });
  } else {
    console.error('토큰이 없습니다. 로그인 후 다시 시도해주세요.');
  }
});

const deleteComment = (reviewId) => {
  if(confirm("정말로 리뷰를 삭제하시겠습니까")){
    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/movies/detail/${movieId}/create_review/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then(res => {
      console.log(res.data.message)
      reviews.value = reviews.value.filter(review => review.id !== reviewId)
    })
    .catch(err => {
      console.log(err)
    })
  }
}
</script>

<style scoped>
.comment-section {
  margin-top: 20px;
}

.comment-title {
  margin-bottom: 20px;
  font-family: 'Noto Sans KR', sans-serif;
}

.no-comments {
  text-align: center;
  font-size: 1.2rem;
  color: #777;
  font-family: 'Noto Sans KR', sans-serif;
}

.review-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.review-card {
  background: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.review-card:hover {
  transform: translateY(-5px);
}

.review-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.review-content {
  font-size: 1rem;
  margin-bottom: 10px;
}

.rating {
  margin-bottom: 10px;
}

.filled-star {
  color: gold;
}

.empty-star {
  color: lightgray;
}

.review-author, .review-date {
  font-size: 0.9rem;
  color: #555;
}
</style>
