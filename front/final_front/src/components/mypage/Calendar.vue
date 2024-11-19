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
             @click="openEmojiModal(date)"
           >
             <span class="date-number">{{ date.date }}</span>
             <div v-if="date.emoji" class="emoji">
               <img :src="date.emoji" alt="emoji" class="emoji-image" />
             </div>
           </div>
         </div>
       </div>
     </div>
 
     <!-- 이모지 선택 모달 -->
     <div v-if="showEmojiModal" class="modal">
       <div class="modal-content">
         <h3>이모지 선택</h3>
         <button v-for="emoji in emojis" :key="emoji" @click="selectEmoji(emoji)">
           <img :src="emoji" alt="emoji" class="emoji-select-image" />
         </button>
         <button @click="showEmojiModal = false">Close</button>
       </div>
     </div>
   </div>
 </template>
 
 <script>
 import { ref } from 'vue';
 
 // 이미지 파일 import
 import happy from '@/assets/images/happy.jpg';
 import sad from '@/assets/images/sad.jpg';
 import angry from '@/assets/images/angry.jpg';
 import sleepy from '@/assets/images/sleepy.jpg';
 import excited from '@/assets/images/excited.jpg';
 import calm from '@/assets/images/calm.jpg';
 
 
 export default {
   name: 'App',
   components: {

   },
   setup() {
     const today = new Date();
     const year = ref(today.getFullYear());
     const month = ref(today.getMonth());
     const days = ['일', '월', '화', '수', '목', '금', '토'];
     const showEmojiModal = ref(false);
     const selectedDate = ref(null);
     const emojis = [happy, sad, angry, sleepy, excited, calm];
     const dates = ref([]);
 
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
           dateKey: `${year.value}-${month.value - 1}-${lastDatePrevMonth - i}`,
         });
       }
       // 현재 달의 날짜 추가
       for (let i = 1; i <= lastDate; i++) {
         dates.value.push({
           date: i,
           isCurrentMonth: true,
           emoji: null,
           dateKey: `${year.value}-${month.value}-${i}`,
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
         month.value === today.getMonth() &&
         year.value === today.getFullYear()
       );
     };
 
     // 이모지 선택 모달 열기
     const openEmojiModal = (date) => {
       selectedDate.value = date;
       showEmojiModal.value = true;
     };
 
     // 이모지 선택
     const selectEmoji = (emoji) => {
       if (selectedDate.value) {
         selectedDate.value.emoji = emoji; 
       }
       showEmojiModal.value = false;
     };
 
     createCalendar();
 
     return {
       year,
       month,
       days,
       dates,
       showEmojiModal,
       emojis,
       prevMonth,
       nextMonth,
       goToday,
       isToday,
       openEmojiModal,
       selectEmoji,
     };
   },
 };
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
 