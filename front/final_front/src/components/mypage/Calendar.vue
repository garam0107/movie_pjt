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
        <input type="text" v-model="diaryTitle" placeholder="제목" />
        <textarea v-model="diaryContent" placeholder="내용"></textarea>
        <div class="emoji-selection">
          <h4>이모지 선택</h4>
          <button v-for="emoji in emojis" :key="emoji" @click="selectEmoji(emoji)">
            <img :src="emoji" alt="emoji" class="emoji-select-image" />
          </button>
        </div>
        <div class="modal-actions">
          <button @click="submitDiary">저장</button>
          <button @click="closeModal">닫기</button>
        </div>
      </div>
    </div>

  <div v-if="detailDiaryModal" class="modal">
  <!-- 상세 모달 내용 -->
   <div class="modal-content">
     <h3> {{selectedDate.dateKey}}</h3>
     <h1>{{ diaryTitle }}</h1>
     <h3>{{ diaryContent }}</h3>
     <h3>당신의 감정은? {{gpt_emotion}}</h3>
     <RouterLink  :to="{ name: 'detail', params: { movie_id: recommend_movieID1 } }">
       <p >첫번째 추천 영화: {{ recommend_movies[0] }}</p>
    </RouterLink>
    <RouterLink  :to="{ name: 'detail', params: { movie_id: recommend_movieID2 } }">
      <p>두번째 추천 영화: {{ recommend_movies[1] }}</p>
    </RouterLink>
     <p>{{recommend_reasons1}}</p>
     <p>{{ recommend_reasons2 }}</p>
     <p>{{ gpt_comment }}</p>
     <div class="modal-actions">
       <button @click="detailDiaryModal = false">닫기</button>
     </div>
     <h1></h1>
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
const selectedDate = ref(null);
const emojis = [happy, sad, angry, sleepy, excited, calm];
const dates = ref([]);
const diaryTitle = ref('');
const diaryContent = ref('');
const selectedEmoji = ref(null);
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




// 다이어리 작성 모달 열기
// const openDiaryModal = (date) => {

//     selectedDate.value = date;
//     showDiaryModal.value = true;
// };
const gpt_comment = ref('')
const recommend_movies = ref([])
const recommend_reasons1 = ref('')
const recommend_reasons2 = ref('')
const recommend_movieID1 = ref('')
const recommend_movieID2 = ref('')
const gpt_emotion = ref('')

const openDiaryModal = (date) => {
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



// 이모지 선택
const selectEmoji = (emoji) => {
  selectedEmoji.value = emojiMap[emoji] || null; // 매핑해서 경로 바꿔주기 
  console.log(selectedEmoji.value)
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
  // if (!user_pk.value) {
  //   console.error('사용자 ID가 존재하지 않습니다.');
  //   return;
  // }

  // 인증 토큰이 있는지 확인
  
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

// 컴포넌트가 마운트될 때 달력 생성
onMounted(() => {
  createCalendar();
});
</script>




 
 <style>
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
 </style>
 