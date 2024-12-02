<template>
  <div class="comments-section">
    <div class="comments-grid">
      <div 
        v-for="(comment, index) in limitedComments" 
        :key="index" 
        class="comment-card"
        @mousemove="handleMouse"
        @mouseleave="resetMouse"
        @click="openModal(comment)">
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
              <p class="movie-content">{{ shortenedContent(comment.content) }}</p>
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
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content modal-form-style">
        <button class="close-button" @click="closeModal">&times;</button>
        <form class="modal-form">
          <div class="form-group">
            <label for="userId" class="user-modal">{{selectedComment.review_user_id}}님이 작성한 코멘트 📜</label>
          </div>
          <div class="form-group">
            <label for="title">Title</label>
            <input type="text" id="title" :value="selectedComment.title" readonly>
          </div>
          <div class="form-group">
            <label for="content">Content</label>
            <textarea id="content" :value="selectedComment.content" readonly></textarea>
          </div>
          <div class="form-group">
            <label for="rating">Rating</label>
            <div class="modal-rating">
              <span
              v-for="star in 5"
              :key="star"
              :class="['star', { filled: star <= Number(selectedComment.rating) }]"
              >★</span>
            </div>
          </div>
        </form>
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
const isModalOpen = ref(false);
const selectedComment = ref(null);

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
  return comments.value.slice(0, 5); // 최신 4개의 댓글만 반환
});

// 내용이 너무 길 경우 ...으로 축약하는 메서드
const shortenedContent = (content) => {
  const maxLength = 10; // 최대 길이 설정
  if (content.length > maxLength) {
    return content.slice(0, maxLength) + '...';
  }
  return content;
};

// 마우스 이동 효과 추가
const handleMouse = (event) => {
  const card = event.currentTarget;
  const { offsetWidth: width, offsetHeight: height } = card;
  const { offsetX: x, offsetY: y } = event;
  const moveX = (x / width) * 30 - 15;
  const moveY = (y / height) * 30 - 15;
  card.style.transform = `rotateX(${moveY}deg) rotateY(${moveX}deg)`;
  card.style.boxShadow = `0 20px 40px rgba(0, 0, 0, 0.2), 0 0 30px rgba(255, 0, 150, 0.5)`; // 무지개빛 그림자 효과 추가
};

// 마우스가 카드에서 떠날 때 효과 초기화
const resetMouse = (event) => {
  const card = event.currentTarget;
  card.style.transform = 'rotateX(0deg) rotateY(0deg)';
  card.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.1)';
};

// 모달 열기
const openModal = (comment) => {
  selectedComment.value = comment;
  isModalOpen.value = true;
};

// 모달 닫기
const closeModal = () => {
  isModalOpen.value = false;
  selectedComment.value = null;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Parkinsans:wght@300..800&display=swap');
.comments-section {
  max-width: 1200px;
  padding: 2px;
}

h2 {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 20px;

}

.comments-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.comment-card {
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  height: auto;
  transition: transform 0.2s ease-out, box-shadow 0.2s ease-out; /* 부드러운 이동 및 그림자 효과 */
  cursor: pointer;
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
  text-decoration: none;
  color: inherit;
  display: inline-block;
}

.review-user {
  font-size: 1rem;
  font-weight: bold;
  color: #333;
  font-family: "Parkinsans", sans-serif;
}

.movie-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background: #fffdfa;
  border: 1px dashed #ddd;
  margin: 5px;
}

.poster {
  width: 100%;
  height: 150px;
  object-fit: cover;
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
  font-family: "Noto Sans KR", sans-serif;
}

.movie-content {
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 10px 0;
  flex-grow: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: "Noto Sans KR", sans-serif;
}

.rating {
  display: flex;
  gap: 2px;
  justify-content: flex-start;
  margin-top: auto;
}

.star {
  font-size: 1.2rem;
  color: #ddd;
}

.star.filled {
  color: #ffd700;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  width: 100%;
  position: relative;
}

.modal-form-style {
  background: #f8f3e8;
  padding: 30px;
  border-radius: 15px;
  border: 2px solid #e5b299;
  box-shadow: 10px 10px 0 #f4a261;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 1rem;
  color: #333;
  font-family: 'Noto Sans KR', sans-serif;
}

input[type="text"],
textarea {
  border: none;
  border-bottom: 2px solid #333;
  background: none;
  padding: 5px;
  font-size: 1rem;
  color: #333;
  outline: none;
  resize: none;
  font-family: 'Noto Sans KR', sans-serif;
}
textarea {
  height: 140px;
}
.modal-rating {
  display: flex;
  gap: 2px;
  justify-content: flex-start;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.user-modal{
  font-size: large;
}

@media (max-width: 900px) {
  .comments-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>