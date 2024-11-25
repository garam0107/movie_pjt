<template>
  <div id="app">
    <div v-if="isMyPage || (!isMyPage && is_public)" class="calendar">
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
            :data-date-key="date.dateKey"
            :class="{ today: isToday(date), otherMonth: !date.isCurrentMonth }"
            @click="openDiaryModal(date)"
          >
            <span class="date-number">{{ date.date }}</span>
            <div v-if="date.emoji" class="emoji">
              <img :src="reverseEmojiMap[date.emoji]" alt="emoji" class="emoji-image" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <h2 class="not-ispublic">비공개 계정입니다 🔒</h2>
    </div>

  <!-- 로딩 애니메이션 (햄스터) -->
  <div v-if="isLoading" class="loading-hamster">
      <div aria-label="Orange and tan hamster running in a metal wheel" role="img" class="wheel-and-hamster">
        <div class="wheel"></div>
        <div class="hamster">
          <div class="hamster__body">
            <div class="hamster__head">
              <div class="hamster__ear"></div>
              <div class="hamster__eye"></div>
              <div class="hamster__nose"></div>
            </div>
            <div class="hamster__limb hamster__limb--fr"></div>
            <div class="hamster__limb hamster__limb--fl"></div>
            <div class="hamster__limb hamster__limb--br"></div>
            <div class="hamster__limb hamster__limb--bl"></div>
            <div class="hamster__tail"></div>
          </div>
        </div>
        <div class="spoke"></div>
      </div>
    </div>


    <!-- 다이어리 작성 모달 -->
    <div v-if="showDiaryModal && !isLoading" class="modal">
    <div class="modal-content">
    <h3>오늘 당신의 감정은? ✏️</h3>
    <div class="form-group">
      <input type="text" v-model="diaryTitle" placeholder="제목" class="form-input" />
    </div>
    <div class="form-group">
      <textarea v-model="diaryContent" placeholder="내용" class="form-textarea"></textarea>
    </div>
    <div class="emoji-selection">
      <h4>감정 선택</h4>
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
    <div class="modal-diary-content">
      <div class="diary-header">
        <h3 class="diary-date">{{ selectedDate.dateKey }}</h3>
        <h1 class="diary-title">{{ diaryTitle }}</h1>
      </div>
      <div class="diary-content">
        <p>{{ diaryContent }}</p>
      </div>
    </div>

    <div class="detail-modal-diary">
      <div class="movie-recommendations">
        <h4>오늘의 영화 추천</h4>
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
      <div class="modal-actions2">
        <div v-if="currentuser == props.userData.username">
          <button @click="openEditModal" class="my-button" v-if="selectedDate.dateKey === Diary_today">수정</button>
          <button @click="openDeleteModal" class="my-button">삭제</button>      
        </div>
        <button @click="closeDiaryModal" class="close-button">닫기</button>
      </div>
    </div>
  </div>
</div>

<!-- 다이어리 수정 모달 -->
<div v-if="showEditDiaryModal && !isLoading" class="modal">
  <div class="modal-content">
    <h3>오늘의 일기 수정 ✏️</h3>
    <div class="form-group">
      <input type="text" v-model="editDiaryTitle" placeholder="제목" class="form-input" />
    </div>
    <div class="form-group">
      <textarea v-model="editDiaryContent" placeholder="내용" class="form-textarea"></textarea>
    </div>
    <div class="emoji-selection">
      <h4>감정 선택</h4>
      <div class="emoji-container">
        <button
          v-for="emoji in emojis"
          :key="emoji"
          @click="selectEmoji2(emoji)"
          :class="{ 'emoji-selected': editSelectedEmoji === emoji }"
          class="emoji-button"
        >
          <img :src="emoji" alt="emoji" class="emoji-select-image" />
        </button>
      </div>
    </div>
    <div class="modal-actions">
      <button @click="updateDiary(props.userData.username, my_diary_pk)" class="submit-button">저장</button>
      <button @click="closeEditModal" class="cancel-button">닫기</button>
    </div>
  </div>
</div>




<!-- 다이어리 삭제 모달 -->
<div v-if="showDeleteConfirmModal" class="modal">
  <div class="modal-content">
    <h3>정말 삭제하시겠습니까?</h3>
    <div class="modal-actions">
      <button @click="confirmDelete" class="submit-button">네</button>
      <button @click="closeDeleteModal" class="cancel-button">아니오</button>
    </div>
  </div>
</div>
</div>
</template>

 
<script setup>
import { ref, watch, onMounted,computed } from 'vue';
import axios from 'axios';
import { useRouter,useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/counter';
// 이미지 파일 import
import happy from '@/assets/images/happy.jpg';
import sad from '@/assets/images/sad.jpg';
import angry from '@/assets/images/angry.jpg';
import sleepy from '@/assets/images/sleepy.jpg';
import excited from '@/assets/images/excited.jpg';
import calm from '@/assets/images/calm.jpg';
import router from '@/router';

// defineProps는 setup 함수 바깥에서 선언
const props = defineProps({
  userData: Object,
});

const store = useMovieStore()
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
const is_public = props.userData.is_public
const route = useRoute()
const currentuser = store.userId
const isMyPage = computed(() => String(store.userId) === String(route.params.user_id));
const isLoading = ref(false)

const reverseEmojiMap = {
  'emotions/angry.jpg': angry,
  'emotions/calm.jpg': calm,
  'emotions/excited.jpg': excited,
  'emotions/happy.jpg': happy,
  'emotions/sad.jpg': sad,
  'emotions/sleepy.jpg': sleepy,
};

const emojiMap = {
  '/src/assets/images/angry.jpg': 'emotions/angry.jpg',
  '/src/assets/images/calm.jpg': 'emotions/calm.jpg',
  '/src/assets/images/excited.jpg': 'emotions/excited.jpg',
  '/src/assets/images/happy.jpg': 'emotions/happy.jpg',
  '/src/assets/images/sad.jpg': 'emotions/sad.jpg',
  '/src/assets/images/sleepy.jpg': 'emotions/sleepy.jpg',
};



const fetchMonthlyEmojis = async (username, year, month) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/diaries/${username}/${year}/${month}/`, {
      headers: { Authorization: `Token ${token}` }
    });

    // 반환된 데이터가 리스트일 경우 바로 사용하도록 처리
    if (Array.isArray(response.data)) {
      return response.data; // 이 데이터는 [{ date: '2024-11-05', mood_emoji: 'emotions/happy.jpg' }, ...] 형식이어야 합니다.
    } else {
      console.error('서버에서 예상치 못한 데이터 형식이 반환되었습니다.');
      return [];
    }
  } catch (error) {
    console.error('이모지 데이터를 가져오는 데 실패했습니다:', error);
    return [];
  }
};

const updateCalendarWithEmojis = (calendarDates, emojiData) => {
  emojiData.forEach(({ date, mood_emoji }) => {
    const targetDate = calendarDates.find((d) => d.dateKey === date);
    if (targetDate) {
      targetDate.emoji = mood_emoji; // 날짜 객체에 이모지를 추가
    }
  });
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
const prevMonth = async () => {
  if (month.value === 0) {
    month.value = 11;
    year.value -= 1;
  } else {
    month.value -= 1;
  }
  createCalendar();


  const emojiData = await fetchMonthlyEmojis(props.userData.username, year.value, month.value + 1);
  updateCalendarWithEmojis(dates.value, emojiData);
};

// 다음 달로 이동
const nextMonth = async () => {
  if (month.value === 11) {
    month.value = 0;
    year.value += 1;
  } else {
    month.value += 1;
  }
  createCalendar();

  const emojiData = await fetchMonthlyEmojis(props.userData.username, year.value, month.value + 1);
  updateCalendarWithEmojis(dates.value, emojiData);
};

// 오늘 날짜로 이동
const goToday = async () => {
  year.value = today.getFullYear();
  month.value = today.getMonth();
  createCalendar();

  const emojiData = await fetchMonthlyEmojis(props.userData.username, year.value, month.value + 1);
  updateCalendarWithEmojis(dates.value, emojiData);
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
const my_diary_pk = ref(null)

const openDiaryModal = (date) => {


  const clickedDate = new Date(year.value, month.value, date.date,12);

  const formattedClickedDate = clickedDate.toISOString().split('T')[0];
  
 
  selectedDate.value = date; // 선택한 날짜 저장


  fetchDiaryByDate(props.userData.username, selectedDate.value.dateKey)
    .then((response) => {
      my_diary_pk.value = response.data.id
      if (response.data.exists === false && formattedClickedDate !== Diary_today) {
        // 다이어리가 없는 경우: 작성 모달 열기

        alert('당일에만 다이어리를 작성할 수 있습니다.')
        return
      }else if(response.data.exists === false && formattedClickedDate === Diary_today){
        if(props.userData.username !== currentuser){
          alert('본인 페이지에서만 다이어리를 작성할 수 있습니다.')
          return
        }
        showDiaryModal.value = true; // 작성 모달 열기
        detailDiaryModal.value = false; // 상세 모달 닫기
      }

      else {
        // console.log(response.data)
        // 다이어리가 있는 경우: 상세 모달 열기
        console.log('오늘 데이터',selectedDate.value)
        diaryTitle.value = response.data.title;
        diaryContent.value = response.data.content;
        selectedEmoji.value = response.data.mood_emoji;
        gpt_comment.value = response.data.gpt_comment
        console.log(selectedEmoji.value)
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

const selectEmoji2 = (emoji) => {
  editSelectedEmoji.value = emojiMap[emoji] || null; // 매핑된 경로로 저장

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
const submitDiary = async () => {
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




  
  if (!token) {
    alert('로그인이 필요합니다.');
    return;
  }
  
  isLoading.value = true
  // 다이어리 작성 API 호출
  try {
    const response = await axios.post(
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
    );

    selectedDate.value.emoji = selectedEmoji.value
    // 다이어리 저장 후 달력 갱신
    createCalendar();
    const emojiData = await fetchMonthlyEmojis(props.userData.username, year.value, month.value + 1);
    updateCalendarWithEmojis(dates.value, emojiData);


    // 모달 초기화 및 닫기
    diaryTitle.value = '';
    diaryContent.value = '';
    selectedEmoji.value = null;
    showDiaryModal.value = false;
    router.go(0)
  } catch (error) {
    
    console.log("오류", error.response.data)
    console.error('다이어리 저장 실패:', error);
  }finally{
    isLoading.value=false
  }
};

// 하이라이트 표시
const highlightDate = (dateKey) => {
  // 달력에 있는 모든 날짜 요소를 찾습니다.
  const dateElements = document.querySelectorAll('.date');

  // 각 날짜 요소를 반복하며 우리가 찾는 날짜와 일치하는 요소를 찾습니다.
  dateElements.forEach((dateElement) => {
    if (dateElement.dataset.dateKey === dateKey) {
      // 찾은 날짜 요소에 하이라이트 클래스를 추가합니다.
      dateElement.classList.add('highlight');
    } else {
      // 나머지 날짜 요소에서는 하이라이트를 제거합니다.
      dateElement.classList.remove('highlight');
    }
  });
};


// 다이어리 수정

const showEditDiaryModal = ref(false);
const editDiaryTitle = ref('');
const editDiaryContent = ref('');
const editSelectedEmoji = ref('');



const updateDiary = (user_username, diary_pk) => {
  // 수정된 데이터 정의


  const updatedData = {
    title: editDiaryTitle.value,        // 사용자가 입력한 제목
    content: editDiaryContent.value,    // 사용자가 입력한 내용
    mood_emoji: editSelectedEmoji.value, // 사용자가 선택한 감정 이모지
  };
  console.log('수정할 데이터:', updatedData);
  // 수정 함수 호출
  isLoading.value = true
  store.updateDiary(user_username, diary_pk, updatedData)
  .then((res) => {
    console.log('다이어리 수정 성공:', res.data);
    alert('다이어리가 성공적으로 수정되었습니다.');

    // 모달 닫기
    showEditDiaryModal.value = false;
    detailDiaryModal.value = false;

    // 달력 데이터 새로고침
    createCalendar();

    // 수정된 날짜 하이라이트
    const updatedDateKey = selectedDate.value.dateKey; // 수정된 날짜의 dateKey 사용
    highlightDate(updatedDateKey);
    router.go(0)
  })
  .catch((err) => {
    console.log(err.data)
    console.log(err.response.data)
    console.error('다이어리 수정 실패:', err);
    alert('다이어리 수정 중 문제가 발생했습니다.');
  }).finally (() =>{
    isLoading.value = false
  })

};

const openEditModal = () => {
  // 수정하려는 다이어리의 기존 데이터를 수정 모달로 전달
  editDiaryTitle.value = diaryTitle.value;      // 기존 제목
  editDiaryContent.value = diaryContent.value;  // 기존 내용
  editSelectedEmoji.value = selectedEmoji.value; // 기존 선택된 이모지

  // 수정 모달을 열기
  showEditDiaryModal.value = true;
};


const closeEditModal = () => {
  editDiaryTitle.value = '';
  editDiaryContent.value = '';
  editSelectedEmoji.value = '';
  showEditDiaryModal.value = false;
};



// 다이어리 삭제
const showDeleteConfirmModal = ref(false)

const openDeleteModal = () => {
  showDeleteConfirmModal.value = true
}
const closeDeleteModal = () => {
  showDeleteConfirmModal.value = false
}


const deleteDiary = (username,pk) =>{
  store.deleteDiary(username,pk)
  alert('다이어리가 삭제되었습니다.')
  detailDiaryModal.value = false
  router.go(0)
}

const confirmDelete = () => {
  console.log(props.userData.username,my_diary_pk.value)
  deleteDiary(props.userData.username, my_diary_pk.value)

  closeDeleteModal()
}
watch(dates, (newDates) => {
  // console.log("dates가 변경되었습니다:", newDates);
  // 이 시점에서 Vue가 배열의 변경을 감지하고 UI를 업데이트할 것임
}, { deep: true });

// 컴포넌트가 마운트될 때 달력 생성
onMounted(async () => {
  createCalendar();

  const emojiData = await fetchMonthlyEmojis(props.userData.username, year.value, month.value + 1);
  if (emojiData.length > 0) {
    updateCalendarWithEmojis(dates.value, emojiData);
  }
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
  justify-content: center;
  align-items: center;
  gap: 10px; /* 버튼 사이 간격 */
}

.nav-btn {
  background-color: #f4c895; /* 따뜻한 주황색 배경 */
  color: #fff; /* 흰색 텍스트 */
  border: none;
  border-radius: 50%; /* 버튼을 동그랗게 */
  height: 20px;
  font-size: 0.7rem; /* 화살표 및 텍스트 크기 */
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 약간의 그림자 효과 */
  transition: all 0.3s ease; /* 부드러운 애니메이션 */
}

.nav-btn:hover {
  background-color: #f1a447; /* 호버 시 더 짙은 주황색 */
  transform: scale(1.1); /* 버튼이 살짝 커짐 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2); /* 그림자 강조 */
}

.nav-btn:active {
  transform: scale(0.95); /* 클릭 시 버튼이 살짝 눌리는 효과 */
}


.go-today {
  font-size: 0.7rem; /* Today 버튼의 텍스트 크기 */
  border-radius: 10px; /* Today 버튼은 약간 둥글게 */
  background-color: #f4c895;
}

.go-today:hover {
  background-color: #f1a447;
}

.go-today:active {
  transform: scale(0.95);
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
   font-family: 'Noto Serif KR', serif; 
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
 
  /* ㅇㅇ */
 .modal-content {
  background-color: #fffaf0;
  border: 2px solid #f4c895;
  border-radius: 15px;
  width: 30%;
  padding: 20px;
  font-family: 'Noto Serif KR', serif; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
}

.modal-content h3 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
}


.form-textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  background-color: #fffaf0;
  resize: none;
}

.emoji-selection h4 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.emoji-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.emoji-button:hover {
  transform: scale(1.2);
}

.emoji-select-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid transparent;
}

.emoji-selected .emoji-select-image {
  border: 2px solid #f4c895;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.modal-actions2 {
  display: flex;
  /* justify-content: space-between; */
  margin-top: 20px;
}

.submit-button,
.cancel-button {
  width: 25%;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-button {
  background-color: #f4c895;
  color: #fff;
}

.submit-button:hover {
  background-color: #f1a447;
}

.cancel-button {
  background-color: #d8d8d8;
  color: #333;
}

.cancel-button:hover {
  background-color: #b8b8b8;
}

/* ㅇㅇ */
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


h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 90%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafafa;
  font-family: 'Noto Serif KR', serif; 
  color: #4a4a4a;  
}

.form-input:focus {
  border-color: #fe7547;
  box-shadow: 0 0 5px rgba(255, 0, 127, 0.3);
}

.form-textarea {
  width: 90%;
  height: 150px;
  padding: 15px;
  font-size: 1rem;
  border-radius: 8px;
  outline: none;
  resize: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafafa;
  font-family: 'Noto Serif KR', serif; 
  color: #4a4a4a; 
}

.form-textarea:focus {
  border-color: #fe7547;
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
  grid-template-columns: repeat(3, 1fr);
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

.submit-button,
.cancel-button {
  width: 48%;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  font-family: 'Noto Serif KR', serif; 
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
  display: flex;
  gap: 20px;
}

/* 다이어리 본문 */
.detail-modal-content {
  background: #fffdfa; /* 종이 같은 기본 색 */
  padding: 30px;
  border-radius: 15px;
  width: 60%;
  max-width: 90%;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  font-family: 'Noto Serif KR', serif; 
  line-height: 1.6;
  text-align: left;
  position: relative;
  background-image: url('https://www.transparenttextures.com/patterns/linen-white.png'); /* 종이 질감 배경 */
  background-size: cover;
  background-repeat: repeat;
  display: flex;
  gap: 20px;
  max-height: 99%;
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
  font-size: 1rem;
  color: #444;
  margin-bottom: 30px;
  white-space: pre-line; /* 줄 바꿈 적용 */
}

/* 영화 추천 섹션 */
.movie-recommendations h4 {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 10px;
  margin-top: 0
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
  font-family: 'Noto Sans KR', sans-serif;
  /* margin-top: 20px; */
  padding: 10px 20px;
  font-size: 0.9rem;
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
  font-family: 'Noto Sans KR', sans-serif;
  padding: 10px 20px;
  font-size: 0.9rem;
  border: none;
  border-radius: 8px;
  background-color: #f28a3a;
  color: white;
  cursor: pointer;
  margin-right: 10px;
}
.highlight {
  border: 2px solid #ff007f; /* 핑크색 테두리 */
  background-color: rgba(255, 0, 127, 0.1); /* 연한 배경색 */
  transform: scale(1.05); /* 살짝 확대 */
  transition: all 0.2s ease-in-out; /* 부드러운 효과 */
}

.modal-diary-content {
  flex: 5;
}

.detail-modal-diary {
  flex: 5;
}

.year-month{
  font-family: 'Noto Serif KR', serif; 
}
.day {
  font-family: 'Noto Serif KR', serif; 
}
.not-ispublic {
  font-family: 'Noto Serif KR', serif; 
  text-align: center;
  padding: 100px;
}
/* 로딩 애니메이션 스타일 추가 */
.wheel-and-hamster {
  --dur: 1s;
  position: relative;
  width: 12em;
  height: 12em;
  font-size: 14px;
}

.wheel,
.hamster,
.hamster div,
.spoke {
  position: absolute;
}

.wheel,
.spoke {
  border-radius: 50%;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.wheel {
  background: radial-gradient(100% 100% at center, hsla(0, 0%, 60%, 0) 47.8%, hsl(0, 0%, 60%) 48%);
  z-index: 2;
}

.hamster {
  animation: hamster var(--dur) ease-in-out infinite;
  top: 50%;
  left: calc(50% - 3.5em);
  width: 7em;
  height: 3.75em;
  transform: rotate(4deg) translate(-0.8em, 1.85em);
  transform-origin: 50% 0;
  z-index: 1;
}

/* 나머지 햄스터 애니메이션 스타일은 그대로 유지 */

/* 로딩 애니메이션 컨테이너 스타일 */
.loading-hamster {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
/* From Uiverse.io by Nawsome */ 
.wheel-and-hamster {
  --dur: 1s;
  position: relative;
  width: 12em;
  height: 12em;
  font-size: 14px;
}

.wheel,
.hamster,
.hamster div,
.spoke {
  position: absolute;
}

.wheel,
.spoke {
  border-radius: 50%;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.wheel {
  background: radial-gradient(100% 100% at center,hsla(0,0%,60%,0) 47.8%,hsl(0,0%,60%) 48%);
  z-index: 2;
}

.hamster {
  animation: hamster var(--dur) ease-in-out infinite;
  top: 50%;
  left: calc(50% - 3.5em);
  width: 7em;
  height: 3.75em;
  transform: rotate(4deg) translate(-0.8em,1.85em);
  transform-origin: 50% 0;
  z-index: 1;
}

.hamster__head {
  animation: hamsterHead var(--dur) ease-in-out infinite;
  background: hsl(30,90%,55%);
  border-radius: 70% 30% 0 100% / 40% 25% 25% 60%;
  box-shadow: 0 -0.25em 0 hsl(30,90%,80%) inset,
		0.75em -1.55em 0 hsl(30,90%,90%) inset;
  top: 0;
  left: -2em;
  width: 2.75em;
  height: 2.5em;
  transform-origin: 100% 50%;
}

.hamster__ear {
  animation: hamsterEar var(--dur) ease-in-out infinite;
  background: hsl(0,90%,85%);
  border-radius: 50%;
  box-shadow: -0.25em 0 hsl(30,90%,55%) inset;
  top: -0.25em;
  right: -0.25em;
  width: 0.75em;
  height: 0.75em;
  transform-origin: 50% 75%;
}

.hamster__eye {
  animation: hamsterEye var(--dur) linear infinite;
  background-color: hsl(0,0%,0%);
  border-radius: 50%;
  top: 0.375em;
  left: 1.25em;
  width: 0.5em;
  height: 0.5em;
}

.hamster__nose {
  background: hsl(0,90%,75%);
  border-radius: 35% 65% 85% 15% / 70% 50% 50% 30%;
  top: 0.75em;
  left: 0;
  width: 0.2em;
  height: 0.25em;
}

.hamster__body {
  animation: hamsterBody var(--dur) ease-in-out infinite;
  background: hsl(30,90%,90%);
  border-radius: 50% 30% 50% 30% / 15% 60% 40% 40%;
  box-shadow: 0.1em 0.75em 0 hsl(30,90%,55%) inset,
		0.15em -0.5em 0 hsl(30,90%,80%) inset;
  top: 0.25em;
  left: 2em;
  width: 4.5em;
  height: 3em;
  transform-origin: 17% 50%;
  transform-style: preserve-3d;
}

.hamster__limb--fr,
.hamster__limb--fl {
  clip-path: polygon(0 0,100% 0,70% 80%,60% 100%,0% 100%,40% 80%);
  top: 2em;
  left: 0.5em;
  width: 1em;
  height: 1.5em;
  transform-origin: 50% 0;
}

.hamster__limb--fr {
  animation: hamsterFRLimb var(--dur) linear infinite;
  background: linear-gradient(hsl(30,90%,80%) 80%,hsl(0,90%,75%) 80%);
  transform: rotate(15deg) translateZ(-1px);
}

.hamster__limb--fl {
  animation: hamsterFLLimb var(--dur) linear infinite;
  background: linear-gradient(hsl(30,90%,90%) 80%,hsl(0,90%,85%) 80%);
  transform: rotate(15deg);
}

.hamster__limb--br,
.hamster__limb--bl {
  border-radius: 0.75em 0.75em 0 0;
  clip-path: polygon(0 0,100% 0,100% 30%,70% 90%,70% 100%,30% 100%,40% 90%,0% 30%);
  top: 1em;
  left: 2.8em;
  width: 1.5em;
  height: 2.5em;
  transform-origin: 50% 30%;
}

.hamster__limb--br {
  animation: hamsterBRLimb var(--dur) linear infinite;
  background: linear-gradient(hsl(30,90%,80%) 90%,hsl(0,90%,75%) 90%);
  transform: rotate(-25deg) translateZ(-1px);
}

.hamster__limb--bl {
  animation: hamsterBLLimb var(--dur) linear infinite;
  background: linear-gradient(hsl(30,90%,90%) 90%,hsl(0,90%,85%) 90%);
  transform: rotate(-25deg);
}

.hamster__tail {
  animation: hamsterTail var(--dur) linear infinite;
  background: hsl(0,90%,85%);
  border-radius: 0.25em 50% 50% 0.25em;
  box-shadow: 0 -0.2em 0 hsl(0,90%,75%) inset;
  top: 1.5em;
  right: -0.5em;
  width: 1em;
  height: 0.5em;
  transform: rotate(30deg) translateZ(-1px);
  transform-origin: 0.25em 0.25em;
}

.spoke {
  animation: spoke var(--dur) linear infinite;
  background: radial-gradient(100% 100% at center,hsl(0,0%,60%) 4.8%,hsla(0,0%,60%,0) 5%),
		linear-gradient(hsla(0,0%,55%,0) 46.9%,hsl(0,0%,65%) 47% 52.9%,hsla(0,0%,65%,0) 53%) 50% 50% / 99% 99% no-repeat;
}

/* Animations */
@keyframes hamster {
  from, to {
    transform: rotate(4deg) translate(-0.8em,1.85em);
  }

  50% {
    transform: rotate(0) translate(-0.8em,1.85em);
  }
}

@keyframes hamsterHead {
  from, 25%, 50%, 75%, to {
    transform: rotate(0);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(8deg);
  }
}

@keyframes hamsterEye {
  from, 90%, to {
    transform: scaleY(1);
  }

  95% {
    transform: scaleY(0);
  }
}

@keyframes hamsterEar {
  from, 25%, 50%, 75%, to {
    transform: rotate(0);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(12deg);
  }
}

@keyframes hamsterBody {
  from, 25%, 50%, 75%, to {
    transform: rotate(0);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(-2deg);
  }
}

@keyframes hamsterFRLimb {
  from, 25%, 50%, 75%, to {
    transform: rotate(50deg) translateZ(-1px);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(-30deg) translateZ(-1px);
  }
}

@keyframes hamsterFLLimb {
  from, 25%, 50%, 75%, to {
    transform: rotate(-30deg);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(50deg);
  }
}

@keyframes hamsterBRLimb {
  from, 25%, 50%, 75%, to {
    transform: rotate(-60deg) translateZ(-1px);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(20deg) translateZ(-1px);
  }
}

@keyframes hamsterBLLimb {
  from, 25%, 50%, 75%, to {
    transform: rotate(20deg);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(-60deg);
  }
}

@keyframes hamsterTail {
  from, 25%, 50%, 75%, to {
    transform: rotate(30deg) translateZ(-1px);
  }

  12.5%, 37.5%, 62.5%, 87.5% {
    transform: rotate(10deg) translateZ(-1px);
  }
}

@keyframes spoke {
  from {
    transform: rotate(0);
  }

  to {
    transform: rotate(-1turn);
  }
}
 </style>
 