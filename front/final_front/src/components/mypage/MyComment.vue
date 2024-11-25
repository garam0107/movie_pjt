<template>
  <div class="comment-section">
    <div v-if="userData?.my_review?.length === 0" class="no-comments">
      <p class="no-comment">리뷰가 없습니다. 리뷰를 작성해보세요 !</p>
    </div>
    <div v-else class="review-container">
      <h3 class="comment-title">{{ userData.nickname }}님의 최근 리뷰 ✏️</h3>
      <div class="review-grid">
        <div
          class="review-card"
          v-for="review in userData.my_review"
          :key="review.movie_title"
          @mousemove="handleMouseMove"
          @mouseleave="handleMouseLeave"
          :style="{'background-image': `url(https://image.tmdb.org/t/p/w500${review.movie_poster_path})`}"
          @click="openReviewModal(review)"
        >
          <div class="card-content">
            <h5 class="review-title">{{ review.title }}</h5>
            <p class="review-content">
              {{ review.content.length > 40 ? review.content.slice(0, 40) + '...' : review.content }}
            </p>
            <div class="rating">
              <span
                v-for="star in 5"
                :key="star"
                :class="{'filled-star': star <= review.rating, 'empty-star': star > review.rating}"
              >
                {{ star <= review.rating ? '⭐' : '☆' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
      <div class="modal-content modal-form-style" @click.stop>
        <button class="close-button" @click="closeModal">X</button>
        <router-link
          :to="{ name: 'detail', params: { movie_id: currentReview.movie_id } }"
          class="movie-title-link"
        >
        <h3 class="movie-title-title">🎦 {{ currentReview.movie_title }}</h3>
        </router-link>
        <p><strong>Title:</strong> {{ currentReview.title }}</p>
        <p><strong>Content:</strong> {{ currentReview.content }}</p>
        <div class="rating2">
          <span
            v-for="star in 5"
            :key="star"
            :class="{'filled-star': star <= currentReview.rating, 'empty-star': star > currentReview.rating}"
          >
            {{ star <= currentReview.rating ? '⭐' : '☆' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

defineProps({
  userData: Object
});

const router = useRouter();

const goDetail = (id) => {
  router.push({ name: 'detail', params: { movie_id: id } });
};

const handleMouseMove = (e) => {
  const card = e.currentTarget;
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  const halfWidth = rect.width / 2;
  const halfHeight = rect.height / 2;

  const rotateX = ((y - halfHeight) / halfHeight) * 15;
  const rotateY = ((x - halfWidth) / halfWidth) * -15;

  card.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
};

const handleMouseLeave = (e) => {
  const card = e.currentTarget;
  card.style.transform = 'rotateY(0deg) rotateX(0deg)';
};

// Modal logic
const isModalOpen = ref(false);
const currentReview = ref({});

const openReviewModal = (review) => {
  currentReview.value = review;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Hahmlet:wght@100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap');

.comment-section {
  margin-top: 20px;
  font-family: Arial, sans-serif;
}

.comment-title {
  margin-bottom: 20px;
  text-align: left;
  padding-left: 10px;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #2c3e50;
  font-family: "Noto Sans KR", sans-serif;
}

.no-comments {
  text-align: center;
  font-size: 1.2rem;
  color: #777;
  font-family: Arial, sans-serif;
}

.review-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  justify-content: center;
  perspective: 1500px;
}

.review-card {
  background-size: cover;
  background-position: center;
  padding: 10px;
  border-radius: 15px;
  position: relative;
  overflow: hidden;
  height: 250px;
  width: 150px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out, box-shadow 0.2s ease-in-out;
  color: #ffffff;
  cursor: pointer;
  background-color: #34495e;

  background-image: linear-gradient(115deg, #0ff 25%, transparent 50%, #f0f 75%, transparent);
  background-blend-mode: overlay;
}

.review-card:hover {
  transform: rotateY(15deg) translateY(-10px) scale(1.05);
  box-shadow: -20px -20px 30px -25px #0ff, 20px 20px 30px -25px #f0f, 0 0 13px 4px rgba(255, 255, 255, 0.3),
    0 55px 35px -20px rgba(0, 0, 0, 0.5);
}

.card-content {
  background: rgba(44, 62, 80, 0.8);
  padding: 10px;
  border-radius: 10px;
  height: 200px;
  display: block;
}

.review-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 10px;
  line-height: 1.3;
  font-family: "Noto Sans KR", sans-serif;
}

.movie-title {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: #ecf0f1;
}

.review-content {
  font-size: 0.9rem;
  margin-bottom: 15px;
  line-height: 1.6;
  color: #ecf0f1;
  font-family: "Hahmlet", serif;
  font-optical-sizing: auto;
}

.rating {
  position: absolute;
  bottom: 50px;
  left: 10px;
}

.filled-star {
  color: #f1c40f;
  cursor: pointer;
  font-size: 1.2rem;
  transition: transform 0.2s;
}

.filled-star:hover {
  transform: scale(1.2);
}

.empty-star {
  color: #bdc3c7;
  cursor: pointer;
  font-size: 1.2rem;
  transition: transform 0.2s;
}

.empty-star:hover {
  transform: scale(1.2);
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-form-style {
  background: #f8f3e8;
  padding: 30px;
  border-radius: 15px;
  border: 2px solid #e5b299;
  box-shadow: 10px 10px 0 #f4a261;
}

.modal-content {
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  font-family: 'Noto Sans KR', sans-serif;
  position: relative;
}

.modal-content h3 {
  margin-bottom: 10px;
  font-size: 1.5rem;
  color: #2c3e50;
}

.modal-content p {
  margin-bottom: 10px;
  font-size: 1rem;
  color: #34495e;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #2c3e50;
}
.movie-title-link {
  text-decoration: none;
  color: #3498db;
}

.movie-title-link:hover {
  text-decoration: underline;
}

.movie-title-title {
  font-family: 'Hahmlet', serif;
}

.no-comments{
  font-family: "Noto Sans KR", sans-serif;

}
</style>
