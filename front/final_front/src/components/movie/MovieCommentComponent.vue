<template>
  <div class="comment-section">
    <div class="comment-title">
      <h3>코멘트</h3>
    </div>
    <div v-if="reviews.length === 0" class="no-comments">
      <p>코멘트가 없습니다. 첫 번째 코멘트를 작성해보세요!</p>
    </div>
    <div v-else class="review-grid ">
      <div 
        class="review-card modal-form-style2" 
        v-for="review in reviews" 
        :key="review.id"
        @click="openModal(review)"
      >
        <h5 class="review-title">{{ review.title }}</h5>
        <p class="review-content">{{ shortenedContent(review.content) }}</p>
        <div class="rating">
          <span v-for="star in 5" :key="star" :class="{'filled-star': star <= review.rating, 'empty-star': star > review.rating}">
            {{ star <= review.rating ? '⭐' : '☆' }}
          </span>
        </div>
        <p class="review-author">작성자: {{ review.username }}</p>
        <p class="review-date">작성일: {{ formatDate(review.created_at) }}</p>
        <div v-if="review.username === userData.username">
          <button @click.stop="openUpdateModal(review)" class="updateBtn">수정</button>
          <button @click.stop="deleteComment(review.id)" class="deleteBtn">삭제</button>
        </div>
      </div>
    </div>
    
    <!-- 상세모달 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content modal-form-style">
        <button class="close-button" @click="closeModal">&times;</button>

        
        <h3 @click="godetail(selectedReview.username)" class="review-hover">{{ selectedReview.nickname }}님의 리뷰 📜</h3>
        
        <div class="input-group">
          <label for="title">Title</label>
          <input type="text" :value="selectedReview.title" id="title" class="input-field" readonly>
        </div>
        
        <div class="input-group">
          <label for="content">Content</label>
          <textarea :value="selectedReview.content" id="content" class="input-field2" readonly></textarea>
        </div>

        <div class="input-group">
          <label>Rating</label>
          <div class="rating-container">
            <span 
              v-for="star in 5" 
              :key="star" 
              :class="{'filled-star': star <= selectedReview.rating, 'empty-star': star > selectedReview.rating}"
            >
              ★
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>

<!-- 수정 모달 -->
<div v-if="showUpdateModal" class="modal-overlay">
  <div class="modal-content modal-form-style">
    <button class="close-button" @click="closeUpdateModal">&times;</button>

    <h3>리뷰 수정하기 🛠️</h3>

    <div class="input-group">
      <label for="edit-title">Title</label>
      <input 
        type="text" 
        v-model="editReview.title" 
        id="edit-title" 
        class="input-field"
      >
    </div>

    <div class="input-group">
      <label for="edit-content">Content</label>
      <textarea 
        v-model="editReview.content" 
        id="edit-content" 
        class="input-field2"
      ></textarea>
    </div>

    <div class="input-group">
      <label>Rating</label>
      <div class="rating-container">
        <span 
          v-for="star in 5" 
          :key="star" 
          :class="{'filled-star': star <= editReview.rating, 'empty-star': star > editReview.rating}"
          @click="editReview.rating = star"
        >
          ★
        </span>
      </div>
    </div>

    <button @click="updateComment" class="updateBtn2">수정 완료</button>
  </div>
</div>


</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute,useRouter } from 'vue-router';
import { useMovieStore } from '@/stores/counter';

const router = useRouter()
const reviews = ref([])
const route = useRoute()
const movieId = route.params.movie_id
const userData = ref({})
const store = useMovieStore()
const showModal = ref(false)
const showUpdateModal = ref(false)
const selectedReview = ref({ title: '', content: '', rating: 0, username: '' })
const editReview = ref({ id: null, title: '', content: '', rating: 0 })
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
  const date = new Date(dateString);
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`;
};

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

// 리뷰 수정 함수
const updateComment = () => {
  axios({
    method: 'put',
    url: `http://127.0.0.1:8000/movies/detail/${movieId}/create_review/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      title: editReview.value.title,
      content: editReview.value.content,
      rating: editReview.value.rating
    }
  })
  .then(response => {
    console.log(response.data.message);
    // 로컬 데이터 업데이트
    const updatedReview = reviews.value.find(r => r.id === editReview.value.id);
    if (updatedReview) {
      updatedReview.title = editReview.value.title;
      updatedReview.content = editReview.value.content;
      updatedReview.rating = editReview.value.rating;
    }
    closeUpdateModal(); // 모달 닫기
    location.reload(); // 페이지 새로고침
  })
  .catch(err => {
    console.error('리뷰 수정 중 오류가 발생했습니다.', err);
  });
};


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
      console.log(res.data.message);
      reviews.value = reviews.value.filter(review => review.id !== reviewId);
      router.go(0)
    })
    .catch(err => {
      console.log(err);
    });
  }
};

// 모달 열기
const openModal = (review) => {
  selectedReview.value = { ...review };
  showModal.value = true;
};

// 모달 닫기
const closeModal = () => {
  showModal.value = false;
};

// 수정 모달 열기
const openUpdateModal = (review) => {
  editReview.value = { ...review };
  // selectedReview.value = { ...review };
  showUpdateModal.value = true;
};

// 수정 모달 닫기
const closeUpdateModal = () => {
  showUpdateModal.value = false;
};

// 내용이 너무 길 경우 ...으로 축약하는 메서드
const shortenedContent = (content) => {
  const maxLength = 25; // 최대 길이 설정
  if (content.length > maxLength) {
    return content.slice(0, maxLength) + '...';
  }
  return content;
};

const godetail = (user_username) => {
  router.push({name: 'MyPageView', params :{user_id:user_username}})
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
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  cursor: pointer;
}
.modal-form-style {
  background: #f8f3e8;
  border-radius: 15px;
  border: 2px solid #e5b299;
  box-shadow: 10px 10px 0 #f4a261;
}


.review-card:hover {
  transform: translateY(-5px);
}

.review-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 10px;
  margin-top: 0;
}

.review-content {
  font-size: 1rem;
  margin-bottom: 10px;
}

.rating {
  margin-bottom: 10px;
}

.review-author, .review-date {
  font-size: 0.9rem;
  color: #555;
}

/* 버튼 스타일링 */
.updateBtn, .deleteBtn {
  background-color: #fdc394;
  color: #555;
  border: none;
  padding: 6px 8px;
  margin-right: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.9rem;
  font-family: 'Noto Sans KR', sans-serif;
}

.updateBtn2 {
  background-color: #fdc394;
  color: #555;
  border: none;
  padding: 6px 8px;
  margin-right: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.9rem;
  font-family: 'Noto Sans KR', sans-serif;
  margin-top: 10px;
}

.updateBtn:hover, .deleteBtn:hover {
  background-color: #fdae6e;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-form-style2 {
  background: #f8f3e8;
  padding: 10px;
  border-radius: 15px;
  border: 2px solid #e5b299;
  box-shadow: 10px 10px 0 #f4a261;
}

.modal-content {
  font-family: 'Noto Sans KR', sans-serif;
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
  width: 100%;
  position: relative;
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

.input-group {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

.input-field2 {
  height: 140px;
  width: 90%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s;
  font-family: 'Noto Sans KR', sans-serif;
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

.input-field:focus {
  outline: none;
  border-color: #007bff;
}

/* 별점 스타일 */
.rating-container {
  display: flex;
  gap: 5px;
}

.filled-star {
  color: gold;
  cursor: pointer;
  font-size: 1.5rem;
  transition: transform 0.2s;
}

.empty-star {
  color: lightgray;
  cursor: pointer;
  font-size: 1.5rem;
  transition: transform 0.2s;
}
.review-hover{
  cursor: pointer;
  transition: color 0.3s ease;
}
.review-hover:hover {
  color: #ff398b;
}
</style>
