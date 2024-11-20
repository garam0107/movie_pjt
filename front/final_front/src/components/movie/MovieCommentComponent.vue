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
          <button @click="openUpdateModal(review)" class="updateBtn">리뷰 수정</button>
          <button @click="deleteComment(review.id)" class="deleteBtn">리뷰 삭제</button>
        </div>
      </div>
    </div>
  </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3>리뷰 수정</h3>
        <div class="input-group">
          <label for="title">제목:</label>
          <input type="text" v-model="editReview.title" id="title" class="input-field">
        </div>
        
        <div class="input-group">
          <label for="content">내용:</label>
          <textarea v-model="editReview.content" id="content" class="input-field"></textarea>
        </div>

        <div class="input-group">
          <label>별점:</label>
          <div class="rating-container">
            <span 
              v-for="star in 5" 
              :key="star" 
              @mouseover="setTempRating(star)" 
              @mouseleave="resetTempRating"
              @click="setRating(star)"
              :class="{'filled-star': star <= (tempRating || editReview.rating), 'empty-star': star > (tempRating || editReview.rating)}"
            >
            ★
            </span>
          </div>
        </div>

        <div class="modal-buttons">
          <button @click="updateComment" class="saveBtn">저장</button>
          <button @click="closeUpdateModal" class="cancelBtn">취소</button>
        </div>
      </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/counter';
 
const reviews = ref([])
const route = useRoute()
const movieId = route.params.movie_id;
const userData = ref({})
const store = useMovieStore()
const showModal = ref(false)
const editReview = ref({ title: '', content: '', rating: 0 })
const tempRating = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/${movieId}/detail_review/`,
  })
    .then((res) => {
      reviews.value = res.data
    })
    .catch((err) => {
      console.error(err)
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
        console.log('유저 데이터:', res.data)
        userData.value = res.data;
      })
      .catch(err => {
        console.log('마이페이지 정보를 불러오는 중 오류:', err)
      })
  } else {
    console.error('토큰이 없습니다. 로그인 후 다시 시도해주세요.')
  }
})

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
      reviews.value = reviews.value.filter(review => review.id !== reviewId)
    })
    .catch(err => {
      console.log(err)
    })
  }
};

// 모달 열기
const openUpdateModal = (review) => {
  editReview.value = { ...review }; // 기존 리뷰 데이터 복사
  showModal.value = true;
};

// 모달 닫기
const closeUpdateModal = () => {
  showModal.value = false;
  tempRating.value = null; // 모달 닫을 때 임시 별점 초기화
};

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

// 별점 관련 메서드
const setTempRating = (rating) => {
  tempRating.value = rating; // 마우스가 올려진 곳까지의 별점을 임시로 설정
};

const resetTempRating = () => {
  tempRating.value = null; // 마우스가 별에서 벗어나면 임시 별점 초기화
};

const setRating = (rating) => {
  editReview.value.rating = rating; // 클릭한 별점으로 실제 별점 설정
};
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


.review-author, .review-date {
  font-size: 0.9rem;
  color: #555;
}

/* 버튼 스타일링 */
.updateBtn, .deleteBtn {
  background-color: gray;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-right: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.9rem;
}

.updateBtn:hover, .deleteBtn:hover {
  background-color: #555;
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

.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  width: 450px;
  max-width: 90%;
  font-family: 'Noto Sans KR', sans-serif;
}

.input-group {
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s;
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

.filled-star:hover {
  transform: scale(1.2);
}

.empty-star {
  color: lightgray;
  cursor: pointer;
  font-size: 1.5rem;
  transition: transform 0.2s;
}

.empty-star:hover {
  transform: scale(1.2);
}

/* 모달 버튼 스타일 */
.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}


.saveBtn {
  background-color: gray;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.saveBtn:hover {
  background-color: #555;
}

.cancelBtn {
  background-color: gray;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancelBtn:hover {
  background-color: #555;
}
</style>
