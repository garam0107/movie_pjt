<template>
  <div class="mydata-container">
    <div class="profile-header">
      <div class="profile-image">
        <img :src="`/src/assets/${userData.profile_image}`" alt="프로필 이미지">
      </div>
      <div class="user-info">
        <div style="display: flex;">
          <h2>{{ userData.nickname }}</h2>
          <form v-if="isNotMyPage" @submit.prevent="toggleFollow">
            <button v-if="isFollowing" class="followBtn unfollowBtn">언팔로우</button>
            <button v-else class="followBtn">팔로우</button>
          </form>
        </div>
        <p>{{ userData.email }}</p>
        <p>팔로워 {{ userData.followers_count }} | 팔로잉 {{ userData.followings_count }}</p>
      </div>
    </div>
    <div class="user-stats">
      <div class="stat">
        <p class="userstatus">방문자 수: {{ userData.visit_count }}</p>
        <div style="display: flex; justify-content: center;">
          <p class="userstatus">모은 조약돌 수: {{ userData.stone }}</p>
          <img src="@/assets/stone_icon.png" alt="stone icon" class="stone-icon" />
        </div>
      </div>
    </div>
    <div class="actions" v-if="userId == store.userId">
      <button @click="showModal = true">회원정보 수정</button>
      <button @click="showPasswordChange = true">비밀번호 수정</button>
      <button>회원 탈퇴</button>
    </div>
  </div>


  <!-- 회원정보수정 Modal -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h3>회원 정보 수정</h3>
      <div class="form-group">
        <input type="text" v-model="nickname" placeholder="닉네임 수정" class="form-input">
      </div>
      <!-- 프로필 이미지 선택 -->
      <div class="form-group profile-selection">
        <p class="profile-label">프로필 이미지 선택</p>
        <div class="profile-images">
          <label v-for="(image, index) in profileOptions" :key="index" class="profile-option">
            <input 
              type="radio" 
              :value="image.value" 
              v-model="profile_image"
              name="profile_image"
            >
            <img :src="image.src" :alt="image.label" class="profile-img" :title="image.label">
          </label>
          <label class="profile-option">
            <input 
              type="radio" 
              value="" 
              v-model="profile_image"
              name="profile_image"
            >
          </label>
        </div>
      </div>
      <button @click="updateData" type="submit" class="submit-button">회원정보 수정</button>
      <button @click="showModal = false" class="cancel-button">취소</button>
    </div>
  </div>


  <!-- 비밀번호 수정 모달 -->
  



</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { RouterLink } from 'vue-router';
defineProps({
  userData: Object
})
// model
const profileOptions = [
{ value: "profile_images/profile1.jpg", src: new URL('@/assets/profile_images/profile1.jpg', import.meta.url).href, label: "Image 1" },
{ value: "profile_images/profile2.jpg", src: new URL('@/assets/profile_images/profile2.jpg', import.meta.url).href, label: "Image 2" },
{ value: "profile_images/profile3.jpg", src: new URL('@/assets/profile_images/profile3.jpg', import.meta.url).href, label: "Image 3" },
{ value: "profile_images/profile4.jpg", src: new URL('@/assets/profile_images/profile4.jpg', import.meta.url).href, label: "Image 4" },
{ value: "profile_images/profile5.jpg", src: new URL('@/assets/profile_images/profile5.jpg', import.meta.url).href, label: "Image 5" },
{ value: "profile_images/profile6.jpg", src: new URL('@/assets/profile_images/profile6.jpg', import.meta.url).href, label: "Image 6" },
{ value: "profile_images/default_profile.jpg", src: new URL('@/assets/profile_images/default_profile.jpg', import.meta.url).href, label: "Image 7"}
]
const profile_image = ref('')
const showModal = ref('')
const nickname = ref('')
const route = useRoute();
const userId = route.params.user_id // URL에서 user_id를 가져옴
const store = useMovieStore()
const userData = ref({})
const isFollowing = ref(false)

// 내 페이지인지 확인
const isNotMyPage = computed(() => store.userId !== userId)

// 마운트될 때 사용자 정보 불러오기
onMounted(() => {
  if (store.token) {
    // 특정 사용자의 데이터 요청
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId}/mypage/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      userData.value = res.data
      nickname.value = res.data.nickname; // 닉네임 초기화
      profile_image.value = res.data.profile_image; // 프로필 이미지 초기화
    })
    .catch((err) => {
      console.error('유저 정보를 불러오는 중 오류 발생:', err)
    });

    // 팔로우 상태 확인
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId}/follow/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      isFollowing.value = res.data.is_following
      console.log(res.data.is_following)
    })
    .catch((err) => {
      console.error('팔로우 상태를 확인하는 중 오류 발생:', err)
    });
  }
});

const updateData = () => {
  if (!store.token) {
    alert('로그인이 필요합니다.')
    return
  }
  axios({
    method: 'put',
    url: `http://127.0.0.1:8000/accounts/${userId}/update/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      nickname: nickname.value,
      profile_image: profile_image.value,
    },
  })
    .then((res) => {
      userData.value = {
        ...userData.value, // 기존 데이터 유지
        ...res.data, // 응답으로 온 데이터 덮어쓰기
      };
      alert('회원정보가 성공적으로 수정되었습니다.')
      showModal.value = false; // 모달 닫기
    })
    .catch((err) => {
      console.error('회원정보 수정 중 오류:', err)
      alert('회원정보 수정에 실패했습니다.')
    })
}

// 팔로우/언팔로우 기능
const toggleFollow = () => {
  if (!store.token) {
    alert('로그인이 필요합니다.')
    return;
  }

  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/accounts/${userId}/follow/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((res) => {
    if (res.data.message === '팔로우') {
      isFollowing.value = true
      userData.value.followers_count += 1;
    } else if (res.data.message === '언팔로우') {
      isFollowing.value = false
      userData.value.followers_count -= 1;
    }
    console.log(res.data.message)
  })
  .catch((err) => {
    console.error('팔로우/언팔로우 요청 중 오류 발생:', err)
  })
}


</script>


<style scoped>
.followBtn {
  margin-left: 15px;
  font-size: 0.85rem;
  padding: 6px 12px;
  background-color: #28a745;
}

.followBtn:hover {
  background-color: #218838;
}

.followBtn.unfollowBtn {
  background-color: #dc3545;
}

.followBtn.unfollowBtn:hover {
  background-color: #c82333;
}


.mydata-container {
  max-width: 400px;
  margin: 20px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-image img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}

.user-info h2 {
  font-size: 1.5rem;
  margin: 0;
}

.user-info p {
  color: #666;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.stat {
  text-align: center;
}

.stat p {
  margin: 0;
  color: #333;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

button {
  margin: 5px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: gray;
  color: #fff;
  cursor: pointer;
}

button:hover {
  background-color: #666;
}

button:active {
  transform: scale(0.98);
}

.userstatus {
  font-family: "Noto Sans KR", sans-serif;
}

.stone-icon {
  width: 5%;
  margin-left: 5px
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  font-family: "Noto Sans KR", sans-serif;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 380px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.submit-button,
.cancel-button {
  width: 80%;
  margin-top: 10px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
}

.submit-button {
  background-color: #666;
  color: #fff;
  margin-top: 5px;
  font-family: "Noto Sans KR", sans-serif;
}

.cancel-button {
  background-color: #dc3545;
  color: #fff;
  font-family: "Noto Sans KR", sans-serif;
}

.submit-button:hover {
  background-color: gray;
}

.cancel-button:hover {
  background-color: #c82333;
}

.profile-label {
  font-weight: bold;
  margin-bottom: 10px;
  color: #555;
  display: block;
}

.profile-selection {
  width: 100%;
  text-align: left;
}

.profile-images {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 10px;
}

.profile-option {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd;
  cursor: pointer;
  transition: border-color 0.3s;
}

.profile-img:hover {
  border-color: #ff007f;
}

input[type="radio"] {
  display: none; /* 기본 라디오 버튼 숨기기 */
}

input[type="radio"]:checked + .profile-img {
  border-color: #ff007f; /* 선택된 이미지 강조 */
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.3);
}

.form-input {
  width: 80%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafafa;
}
</style>
