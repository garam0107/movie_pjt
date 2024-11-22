<template>
  <div class="comments-section">
    <div class="comments-grid">
      <div v-for="(comment, index) in limitedComments" :key="index" class="comment-card">
        <RouterLink :to="`/mypage/${comment.review_user_id}/`" class="movie-link">
          <div class="profile-section">
            <img :src="`/src/assets/${comment.profile_image}`" alt="프로필 이미지" class="profile-image" />
            <span class="review-user">{{ comment.review_user_id }}</span>
          </div>
        </RouterLink>
        <div class="movie-info">
            <RouterLink :to="`/movie/${comment.movie}`" class="movie-link">
            <img :src="`https://image.tmdb.org/t/p/w500/${comment.poster_path}`" alt="영화 포스터" class="poster" />
            </RouterLink>
            <div class="movie-details">
              <h5 class="movie-title">{{ comment.title }}</h5>
              <p class="movie-content">{{ comment.content }}</p>
              <div class="rating">
                <span
                v-for="star in 5"
                :key="star"
                :class="['star', { filled: star <= Number(comment.rating) }]"
                >★</span>
              </div>
            </div>
          </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';
const props = defineProps ({
  userId: String
})
const store = useMovieStore()
const comments = ref([])
const userData = ref([])
onMounted(() => {
  if (store.token) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${props.userId}/mypage/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      userData.value = res.data;
    })
    .catch((err) => {
      console.error('유저 정보를 불러오는 중 오류 발생:', err);
    });

    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${props.userId}/follow/`,
      headers: {
          Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      console.log(res)
      comments.value = res.data.review
    })
    .catch((err) => {
      console.log(err)
    })
  }
})
// 최신 4개의 코멘트를 가져오는 computed 속성
const limitedComments = computed(() => {
  return comments.value.slice(0, 4); // 최신 4개의 댓글만 반환
});
</script>

<style scoped>
.comments-section {
  max-width: 1200px; /* 전체 섹션의 최대 너비 */
  padding: 2px;
}

h2 {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
}

.comments-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4개의 카드가 가로로 배치되도록 설정 */
  gap: 20px; /* 카드 간격 */
}

.comment-card {
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  height: auto; /* 카드 높이를 내용에 따라 조정 */

}

.comment-card:hover {
  transform: scale(1.05);
}

.profile-section {
  margin-left: 5px;
  display: flex;
  align-items: center;
}

.profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.movie-link {
  text-decoration: none; /* 밑줄 제거 */
  color: inherit; /* 텍스트 색상 상속 */
  display: inline-block; /* 블록 요소로 표시 */
}

.review-user {
  font-size: 1rem;
  font-weight: bold;
  color: #333; /* 사용자 이름 색상 */
}

.movie-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background: #fffdfa; /* 종이 같은 배경 */
  border: 1px dashed #ddd; /* 종이 느낌 테두리 */
  margin: 5px;
  border-radius: 5%;
}

.poster {
  width: 100%;
  height: 150px; /* 일정한 높이로 고정 */
  object-fit: cover; /* 이미지 비율 유지하며 크기 조정 */
  border-radius: 8px;
  margin: 5px;
}

.movie-details {
  margin: 5px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.movie-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin: 0;
}

.movie-content {
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 10px 0;
  flex-grow: 1; /* 내용이 적어도 공간 차지 */
  overflow: hidden; /* 내용이 많을 경우 잘림 */
  text-overflow: ellipsis;
}

.rating {
  display: flex;
  gap: 2px; /* 별 간격 */
  justify-content: flex-start;
  margin-top: auto;
}

.star {
  font-size: 1.2rem;
  color: #ddd; /* 기본 회색 */
}

.star.filled {
  color: #ffd700; /* 노란색 별 */
}

@media (max-width: 900px) {
  .comments-grid {
    grid-template-columns: repeat(2, 1fr); /* 화면 너비가 더 좁아지면 2열로 변경 */
  }
}
</style>