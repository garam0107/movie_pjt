
<template>
  <div class="comment-section">
    <div v-if="userData?.my_review?.length === 0" class="no-comments">
      <p>리뷰가 없습니다.</p>
    </div>
    <div v-else class="review-container">
      <h2 class="comment-title">{{ userData.username }}님의 리뷰</h2>
      <div class="review-grid">
        <div
          class="review-card"
          v-for="review in userData.my_review"
          :key="review.movie_title"
          @mousemove="handleMouseMove"
          @mouseleave="handleMouseLeave"
          @click="goDetail(review.movie_id)"
          :style="{'background-image': `url(https://image.tmdb.org/t/p/w500${review.movie_poster_path})`}"
        >
          <div class="card-content">
            <h4 class="movie-title">{{ review.movie_title }}</h4>
            <h5 class="review-title">{{ review.title }}</h5>
            <p class="review-content">{{ review.content }}</p>
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
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
defineProps({
  userData: Object
});

const router = useRouter()

const goDetail = (id) => {
  router.push({name : 'detail', params: {movie_id : id}})
}


const handleMouseMove = (e) => {
  const card = e.currentTarget;
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left; // 마우스의 카드 내 위치 (x 좌표)
  const y = e.clientY - rect.top;  // 마우스의 카드 내 위치 (y 좌표)

  const halfWidth = rect.width / 2;
  const halfHeight = rect.height / 2;
  
  // 마우스 위치에 따른 각도 계산
  const rotateX = ((y - halfHeight) / halfHeight) * 15; // 카드의 회전 각도
  const rotateY = ((x - halfWidth) / halfWidth) * -15;

  card.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
};

const handleMouseLeave = (e) => {
  const card = e.currentTarget;
  card.style.transform = 'rotateY(0deg) rotateX(0deg)'; // 마우스가 떠났을 때 카드 위치 원래대로
};
</script>
<style scoped>
/* 전체적인 리뷰 섹션 스타일 */
.comment-section {
  margin-top: 20px;
  font-family: Arial, sans-serif;
}

/* 제목 스타일 */
.comment-title {
  margin-bottom: 20px;
  text-align: left;
  padding-left: 10px;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #2c3e50;
}

/* 리뷰가 없을 때 표시할 텍스트 */
.no-comments {
  text-align: center;
  font-size: 1.2rem;
  color: #777;
  font-family: Arial, sans-serif;
}

/* 리뷰 그리드 레이아웃 */
.review-container {
  padding: 10px;
}

/* 리뷰 카드들을 가로로 정렬하고 일정 간격 유지 */
.review-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: space-around;
  perspective: 1500px; /* 카드에 3D 회전 효과를 위한 원근감 추가 */
}

/* 개별 리뷰 카드 스타일 */
.review-card {
  background-size: cover;
  background-position: center;
  padding: 20px;
  border-radius: 15px;
  position: relative;
  overflow: hidden;
  min-height: 450px;
  min-width: 300px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out, box-shadow 0.2s ease-in-out;
  color: #ffffff;
  cursor: pointer;
  background-color: #34495e;
  
  /* 빛나는 효과 */
  background-image: linear-gradient(115deg, #0ff 25%, transparent 50%, #f0f 75%, transparent);
  background-blend-mode: overlay;
}

.review-card:hover {
  transform: rotateY(15deg) translateY(-10px) scale(1.05); /* Y축 회전 및 확대 */
  box-shadow: 
    -20px -20px 30px -25px #0ff, 
    20px 20px 30px -25px #f0f, 
    0 0 13px 4px rgba(255, 255, 255, 0.3), 
    0 55px 35px -20px rgba(0, 0, 0, 0.5); /* 빛나는 그림자 */
}

/* 카드 내부 내용 영역 */
.card-content {
  background: rgba(44, 62, 80, 0.8);
  padding: 20px;
  border-radius: 10px;
}
.movie-title, .review-title, .review-content {
  color: #fff;
}

/* 리뷰 제목 스타일 */
.review-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 10px;
  line-height: 1.3;
}

/* 리뷰 영화 제목 스타일 */
.movie-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: #ecf0f1;
}

/* 리뷰 본문 스타일 */
.review-content {
  font-size: 1.2rem;
  margin-bottom: 15px;
  line-height: 1.6;
  color: #ecf0f1;
}

/* 리뷰의 별점 스타일 */
.rating {
  margin-bottom: 10px;
}

.filled-star {
  color: #f1c40f;
  cursor: pointer;
  font-size: 1.6rem;
  transition: transform 0.2s;
}

.filled-star:hover {
  transform: scale(1.2);
}

.empty-star {
  color: #bdc3c7;
  cursor: pointer;
  font-size: 1.6rem;
  transition: transform 0.2s;
}

.empty-star:hover {
  transform: scale(1.2);
}
</style>

