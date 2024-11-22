<template>
  <div id="app">
    <div class="calendar">
      <div class="header">
        <div class="year-month">{{ year }}년 {{ month + 1 }}월</div>
        <div class="nav">
          <button class="nav-btn go-prev" @click="prevMonth">&lt;</button>
          <button class="nav-btn go-today" @click="goToday">Today</button>
          <button class="nav-btn go-next" @click="nextMonth">&gt;</button>
        </div>
      </div>
      <div class="main">
        <div class="days">
          <div class="day" v-for="day in days" :key="day">{{ day }}</div>
        </div>
        <div class="dates">
          <template>

          </template>
          <div
            class="date"
            v-for="date in dates"
            :key="date.dateKey"
            :class="{ today: isToday(date), otherMonth: !date.isCurrentMonth }"
            @click="openDiaryModal(date)"
          >
            <span class="date-number">{{ date.date }}</span>
            <div v-if="date.emoji" class="emoji">
              <img :src="date.emoji" alt="emoji" class="emoji-image" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 다이어리 작성 모달 -->
    <div v-if="showDiaryModal" class="modal">
    <div class="modal-content">
    <h3>다이어리 작성</h3>
    <div class="form-group">
      <input type="text" v-model="diaryTitle" placeholder="제목" class="form-input" />
    </div>
    <div class="form-group">
      <textarea v-model="diaryContent" placeholder="내용" class="form-textarea"></textarea>
    </div>
    <div class="emoji-selection">
      <h4>이모지 선택</h4>
      <div class="emoji-container">
        <button
          v-for="emoji in emojis"
          :key="emoji"
          @click="selectEmoji(emoji)"
          :class="{ 'emoji-selected': selectedEmoji === emoji }"
          class="emoji-button"
        >
          <img :src="emoji" alt="emoji" class="emoji-select-image" />
        </button>
      </div>
    </div>
      <div class="modal-actions">
        <button @click="submitDiary" class="submit-button">저장</button>
        <button @click="closeModal" class="cancel-button">닫기</button>
      </div>
    </div>
  </div>
  <!-- 다이어리 상세 내용 모달 -->
  <div v-if="detailDiaryModal" class="detail-modal">
  <div class="detail-modal-content">
    <div class="diary-header">
      <h3 class="diary-date">{{ selectedDate.dateKey }}</h3>
      <h1 class="diary-title">{{ diaryTitle }}</h1>
    </div>
    <div class="diary-content">
      <p>{{ diaryContent }}</p>
    </div>
    <div class="movie-recommendations">
      <h4>영화 추천</h4>
      <p style="font-style: bold;">오늘의 감정분석 : {{ gpt_emotion }}</p>
      <div class="recommendation">
        <RouterLink :to="{ name: 'detail', params: { movie_id: recommend_movieID2 } }" class="movie-title">
          <p>🎬 {{ recommend_movies[0] }}</p>
        </RouterLink>
        <p class="reason">{{ recommend_reasons1 }}</p>
      </div>
      <div class="recommendation">
        <RouterLink :to="{ name: 'detail', params: { movie_id: recommend_movieID1 } }" class="movie-title">
          <p>🎬 {{ recommend_movies[1] }}</p>
        </RouterLink>
        <p class="reason">{{ recommend_reasons2 }}</p>
      </div>
    </div>
    <div class="gpt-comment">
      <h4>AI의 한마디</h4>
      <p>{{ gpt_comment }}</p>
    </div>
    
    <div class="modal-actions">
      <button class="my-button">수정</button>
      <button class="my-button">삭제</button>      
      <button @click="closeDiaryModal" class="close-button">닫기</button>
    </div>
  </div>
</div>


  </div>
</template>

 
<script setup>
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// 이미지 파일 import
import happy from '@/assets/images/happy.jpg';
import sad from '@/assets/images/sad.jpg';
import angry from '@/assets/images/angry.jpg';
import sleepy from '@/assets/images/sleepy.jpg';
import excited from '@/assets/images/excited.jpg';
import calm from '@/assets/images/calm.jpg';

// defineProps는 setup 함수 바깥에서 선언
const props = defineProps({
  userData: Object,
});
// watch(
//   () => props.userData,
//   (newUserData) => {
//     if (newUserData && newUserData.pk) {
//       user_id.value = newUserData.pk;
//       console.log('User PK has been updated:', user_pk.value);
//     } else {
//       console.log('userData가 아직 초기화되지 않았습니다:', newUserData);
//     }
//   },
//   { immediate: true }
// );

const today = new Date();
const year = ref(today.getFullYear());
const month = ref(today.getMonth());
const days = ['일', '월', '화', '수', '목', '금', '토'];
const showDiaryModal = ref(false);
const detailDiaryModal = ref(false)
const selectedDate = ref('');
const emojis = [happy, sad, angry, sleepy, excited, calm];
const dates = ref([]);
const diaryTitle = ref('');
const diaryContent = ref('');
const selectedEmoji = ref('');
const Diary_today = new Date().toISOString().split('T')[0]
const token = localStorage.getItem('token');


const emojiMap = {
  '/src/assets/images/angry.jpg': 'emotions/angry.jpg',
  '/src/assets/images/calm.jpg': 'emotions/calm.jpg',
  '/src/assets/images/excited.jpg': 'emotions/excited.jpg',
  '/src/assets/images/happy.jpg': 'emotions/happy.jpg',
  '/src/assets/images/sad.jpg': 'emotions/sad.jpg',
  '/src/assets/images/sleepy.jpg': 'emotions/sleepy.jpg',
};

// 달력 생성
const createCalendar = () => {
  const firstDay = new Date(year.value, month.value, 1).getDay();
  const lastDate = new Date(year.value, month.value + 1, 0).getDate();
  const lastDatePrevMonth = new Date(year.value, month.value, 0).getDate();

  dates.value = [];
  // 이전 달의 남은 날짜 추가
  for (let i = firstDay - 1; i >= 0; i--) {
    dates.value.push({
      date: lastDatePrevMonth - i,
      isCurrentMonth: false,
      emoji: null,
      dateKey: `${year.value}-${month.value === 0 ? 12 : month.value}-${lastDatePrevMonth - i}`,
    });
  }
  // 현재 달의 날짜 추가
  for (let i = 1; i <= lastDate; i++) {
    dates.value.push({
      date: i,
      isCurrentMonth: true,
      emoji: null,
      dateKey: `${year.value}-${month.value+1}-${i}`,
    });
  }
};

// 이전 달로 이동
const prevMonth = () => {
  if (month.value === 0) {
    month.value = 11;
    year.value -= 1;
  } else {
    month.value -= 1;
  }
  createCalendar();
};

// 다음 달로 이동
const nextMonth = () => {
  if (month.value === 11) {
    month.value = 0;
    year.value += 1;
  } else {
    month.value += 1;
  }
  createCalendar();
};

// 오늘 날짜로 이동
const goToday = () => {
  year.value = today.getFullYear();
  month.value = today.getMonth();
  createCalendar();
};

// 오늘인지 확인
const isToday = (date) => {
  return (
    date.isCurrentMonth &&
    date.date === today.getDate() &&
    month.value +1 === today.getMonth() +1 &&
    year.value === today.getFullYear()
  );
};


const fetchDiaryByDate = (username, date) => {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/diaries/${username}/by_date/`,
    params: { date: date },
    headers: { Authorization: `Token ${token}` }
  })
}

const gpt_comment = ref('')
const recommend_movies = ref([])
const recommend_reasons1 = ref('')
const recommend_reasons2 = ref('')
const recommend_movieID1 = ref('')
const recommend_movieID2 = ref('')
const gpt_emotion = ref('')

const openDiaryModal = (date) => {
  const clickedDate = new Date(year.value, month.value, date.date,12);
  console.log(clickedDate)
  const formattedClickedDate = clickedDate.toISOString().split('T')[0];
  console.log(formattedClickedDate)
  if (formattedClickedDate !== Diary_today) {
    alert('다이어리가 없습니다');
    return;
  }
  selectedDate.value = date; // 선택한 날짜 저장
  console.log('선택날짜:', selectedDate.value)
  console.log(selectedDate.value.dateKey)
  
  fetchDiaryByDate(props.userData.username, selectedDate.value.dateKey)
    .then((response) => {
      console.log(response.data)
      if (response.data.exists === false) {
        // 다이어리가 없는 경우: 작성 모달 열기
        showDiaryModal.value = true; // 작성 모달 열기
        detailDiaryModal.value = false; // 상세 모달 닫기
      } else {
        // 다이어리가 있는 경우: 상세 모달 열기
        diaryTitle.value = response.data.title;
        diaryContent.value = response.data.content;
        selectedEmoji.value = response.data.mood_emoji;
        gpt_comment.value = response.data.gpt_comment
     
        recommend_movies.value = response.data.recommend_movie_titles
        recommend_reasons1.value = response.data.recommend_reasons['today_diary_review1']
        recommend_reasons2.value = response.data.recommend_reasons['today_diary_review2']   
        recommend_movieID1.value = response.data.recommend_movie[0]
        recommend_movieID2.value = response.data.recommend_movie[1]
        gpt_emotion.value = response.data.analysis_emotion
        detailDiaryModal.value = true; // 상세 모달 열기
        showDiaryModal.value = false; // 작성 모달 닫기
      }
    })
   .catch((error) => {
  console.error("다이어리 확인 실패:", error);
  if (error.response) {
    // 서버에서의 응답 오류 (4xx, 5xx)
    console.log("서버 응답 오류:", error.response.data);
  } else if (error.request) {
    // 요청이 전송되었지만 응답이 없는 경우
    console.log("서버로부터 응답이 없습니다. 네트워크 문제일 수 있습니다.", error.request);
  } else {
    // 요청 설정 오류 등 기타 오류
    console.log("오류가 발생했습니다:", error.message);
  }
});
};



const closeModal = () => {
  diaryTitle.value = ''
  diaryContent.value = ''
  selectedEmoji.value = null
  showDiaryModal.value = false
}
const closeDiaryModal = () => {
  diaryTitle.value = ''
  diaryContent.value = ''
  selectedEmoji.value = null
  detailDiaryModal.value = false
}

const selectEmoji = (emoji) => {
  selectedEmoji.value = emojiMap[emoji] || null; // 매핑된 경로로 저장

  // 모든 버튼 초기화 후 선택된 버튼에만 클래스 추가
  const emojiButtons = document.querySelectorAll('.emoji-button');
  emojiButtons.forEach((btn) => {
    btn.classList.remove('emoji-selected');
  });

  const selectedButton = Array.from(emojiButtons).find(
    (btn) => btn.querySelector('img').getAttribute('src') === emoji
  );

  if (selectedButton) {
    selectedButton.classList.add('emoji-selected');
  }
};



// 다이어리 저장
const submitDiary = () => {
  if (selectedDate.value.dateKey !== Diary_today) {
    // console.log('오늘날짜' ,selectedDate.value.dateKey)
    // console.log(Diary_today)
    alert('당일에만 다이어리를 작성할 수 있습니다.')
    return
  }


  if (!diaryTitle.value || !diaryContent.value || !selectedEmoji.value) {
    alert('제목, 내용, 이모지를 모두 입력해주세요.');
    return;
  }



  console.log({
    title: diaryTitle.value,
    content: diaryContent.value,
    mood_emoji: selectedEmoji.value,
  });

  
  if (!token) {
    alert('로그인이 필요합니다.');
    return;
  }

  // 다이어리 작성 API 호출
  axios.post(
    `http://127.0.0.1:8000/diaries/${props.userData.username}/`,
    {
      title: diaryTitle.value,
      content: diaryContent.value,
      mood_emoji: selectedEmoji.value,
    },
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  )
    .then((res) => {
      // 선택한 날짜에 이모지 표시
      selectedDate.value.emoji = selectedEmoji.value;
      console.log(res.data)
      // 모달 초기화 및 닫기
      diaryTitle.value = '';
      diaryContent.value = '';
      selectedEmoji.value = null;
      showDiaryModal.value = false;
    })
    .catch((error) => {
      console.log(selectEmoji.value)
      console.log(token)
      console.error('다이어리 저장 실패:', error);
      console.log(error.response.data)
    });
};

// 다이어리 수정


// 다이어리 삭제



// 컴포넌트가 마운트될 때 달력 생성
onMounted(() => {
  createCalendar();
});
</script>




 
 <style scoped>
 .calendar {
   max-width: 900px;
   margin: 20px auto;
   border: 1px solid #ccc;
   border-radius: 5px;
   padding: 20px;
 }
 
 .header {
   display: flex;
   justify-content: space-between;
   align-items: center;
 }
 
 .nav {
   display: flex;
   gap: 5px;
 }
 
 .main {
   margin-top: 20px;
 }
 
 .days {
   display: grid;
   grid-template-columns: repeat(7, 1fr);
   text-align: center;
   font-weight: bold;
 }
 
 .dates {
   display: grid;
   grid-template-columns: repeat(7, 1fr);
   gap: 10px;
 }
 
 .date {
   padding: 25px 15px;
   border-radius: 5px;
   text-align: center;
   cursor: pointer;
   position: relative;
   background-color: #f9f9f9;
 }
 
 .date-number {
   display: block;
   font-size: 0.8rem;
   position: absolute;
   top: 5px;
   left: 5px;
 }
 
 .today {
   background-color: #dff0d8;
 }
 
 .otherMonth {
   color: #aaa;
 }
 
 .emoji {
   position: absolute;
   bottom: 5px;
   right: 5px;
   width: 40px;
   height: 40px;
 }
 
 .emoji-image {
   width: 100%;
   height: 100%;
 }
 
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
   background: white;
   padding: 20px;
   border-radius: 5px;
   width: 300px;
 }
 
 .emoji-select-image {
   width: 30px;
   height: 30px;
   margin: 5px;
 } 

 .modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  font-family: 'Noto Sans KR', sans-serif;
  text-align: center;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 80%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafafa;
}

.form-input:focus {
  border-color: #ff007f;
  box-shadow: 0 0 5px rgba(255, 0, 127, 0.3);
}

.form-textarea {
  width: 80%;
  height: 150px;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  resize: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafafa;
}

.form-textarea:focus {
  border-color: #ff007f;
  box-shadow: 0 0 5px rgba(255, 0, 127, 0.3);
}

.emoji-selection {
  margin-bottom: 20px;
  text-align: left;
}

.emoji-selection h4 {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 10px;
}

.emoji-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 윗줄에 4개 배치 */
  gap: 10px; /* 이모지 간격 */
  justify-content: center;
  margin-bottom: 20px;
  margin-top: 10px;
}

.emoji-button {
  border: none;
  background: none;
  padding: 5px;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.3s;
  display: inline-block;
}

.emoji-button:hover {
  transform: scale(1.1);
}

.emoji-button img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 2px solid transparent; /* 기본 테두리 없음 */
  transition: border-color 0.3s, box-shadow 0.3s;
}

.emoji-button.emoji-selected img {
  border-color: #ff007f; /* 핑크색 테두리 */
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.3); /* 부드러운 그림자 */
  transform: scale(1.15); /* 살짝 확대 */
}

.modal-actions {
  margin-top: 20px;
  display: flex;

}

.submit-button,
.cancel-button {
  width: 48%;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
}

.submit-button {
  background-color: #28a745;
  color: white;
}

.submit-button:hover {
  background-color: #218838;
}

.cancel-button {
  background-color: #dc3545;
  color: white;
}

.cancel-button:hover {
  background-color: #c82333;
}
/* 다이어리 모달 전체 */
.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* 배경 어둡게 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 다이어리 본문 */
.detail-modal-content {
  background: #fffdfa; /* 종이 같은 기본 색 */
  padding: 30px;
  border-radius: 15px;
  width: 650px;
  max-width: 90%;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  font-family: 'Noto Serif KR', serif; /* 다이어리 느낌 나는 폰트 */
  line-height: 1.6;
  text-align: left;
  position: relative;
  background-image: url('https://www.transparenttextures.com/patterns/linen-white.png'); /* 종이 질감 배경 */
  background-size: cover;
  background-repeat: repeat;
}

/* 다이어리 헤더 */
.diary-header {
  text-align: center;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
  /* padding-bottom: 10px; */
}

.diary-date {
  font-size: 1rem;
  color: #888;
  margin-bottom: 5px;
}

.diary-title {
  font-size: 1.8rem;
  color: #333;
  font-weight: bold;
}

/* 다이어리 본문 내용 */
.diary-content {
  font-size: 1.2rem;
  color: #444;
  margin-bottom: 30px;
  white-space: pre-line; /* 줄 바꿈 적용 */
}

/* 영화 추천 섹션 */
.movie-recommendations h4 {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 10px;
}

.recommendation {
  margin-bottom: 15px;
  padding: 7px;
  background: #fffcf2; /* 약간 어두운 종이 느낌 */
  border: 1px dashed #ddd;
  border-radius: 8px;
}

.movie-title {
  font-size: 1.2rem;
  color: #007bff;
  text-decoration: none;
}

.movie-title:hover {
  color: #0056b3;
  text-decoration: underline;
}

.reason {
  font-size: 1rem;
  color: #555;
  margin-top: 5px;
  font-style: italic;
}

/* AI 코멘트 */
.gpt-comment h4 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 10px;
}

.gpt-comment p {
  font-size: 1rem;
  color: #666;
  line-height: 1.5;
  background: #fdfdfd;
  border-left: 4px solid #ff007f; /* 강조 */
  padding: 10px;
  margin: 0;
}

/* 닫기 버튼 */
.close-button {
  /* margin-top: 20px; */
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  background-color: #dc3545;
  color: white;
  cursor: pointer;
}

.close-button:hover {
  background-color: #c82333;
}

.close-button:active {
  transform: scale(0.98);
}
.my-button{
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  background-color: #35b5dc;
  color: white;
  cursor: pointer;
  margin-right: 10px;
}
 </style>
 