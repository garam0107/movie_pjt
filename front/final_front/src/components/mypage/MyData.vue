<template>
  <div class="mydata-container">
    <div class="profile-header">
      <div class="profile-image">
        <img :src="`/src/assets/${props.userData.profile_image}`" alt="프로필 이미지">
      </div>
      <div class="user-info">
        <div style="display: flex;">
          <h2>{{ props.userData.nickname }}</h2>
          <button v-if="isMyPage" @click="isPublicDiary" class="public-btn">{{ userData.is_public ? '공개' : '비공개' }}</button>
          <button v-if="isMyPage" @click="isMovieLike = true" class="public-btn2">❤️</button>
          <form v-if="isNotMyPage" @submit.prevent="toggleFollow">
            <button v-if="isFollowing" class="followBtn unfollowBtn">언팔로우</button>
            <button v-else class="followBtn">팔로우</button>
          </form>
        </div>
        <p>{{ userData.email }}</p>
        <p @click="followModal = true" class="follow-hover">팔로워 {{ localUserData.followers_count }} | 팔로잉 {{ props.userData.followings_count }}</p>
      </div>
    </div>
    <div class="user-stats">
      <div class="stat">
        <p class="userstatus">방문자 수: {{ Math.round(props.userData.visit_count) }}</p>
        <div style="display: flex; justify-content: center;">
          <p class="userstatus">모은 조약돌 수: {{ props.userData.stone }}</p>
          <img src="@/assets/stone_icon.png" alt="stone icon" class="stone-icon" />
        </div>
      </div>
    </div>

    <div class="actions" v-if="isMyPage">
      <button @click="showModal = true">회원정보 수정</button>

      <button @click="showPasswordChange = true">비밀번호 수정</button>
      <div v-if ="showPasswordChange" class = "modal-overlay">
        <div class="modal-content">
          <h2>비밀번호 수정</h2>
          <input type="password" v-model="oldPassword" placeholder="현재 비밀번호" class = "new-form-input">
          <input type="password" v-model="newPassword1" placeholder="새 비밀번호" class = "new-form-input">
          <input type="password" v-model="newPassword2" placeholder="새 비밀번호 확인" class = "new-form-input">
          <div class="modal-actions">
            <button @click="changePassword" class="submit-button">비밀번호 변경</button>
            <button @click="closePasswordModal" class="cancel-button">취소</button>
          </div>
        </div>
      </div>

      <button @click="openDeleteModal">회원 탈퇴</button>
      <div v-if = "showDeleteModal" class = "modal-overlay">
        <div class = "modal-content">
          <h2>회원 탈퇴</h2>
          <p>비밀번호를 입력해주세요.</p>
          <input 
          type="password" 
          v-model="password" 
          placeholder="비밀번호" 
          @keyup.enter="userDelete"
          class = "form-input" 
          >
        <div class="modal-actions">
          <button @click="userDelete" class="submit-button">탈퇴하기</button>
          <button @click="closeDeleteModal" class="cancel-button">취소</button>
        </div>
        </div>
      </div>
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

  <!-- 팔로워, 팔로잉 목록 모달 -->
  <div v-if="followModal" class="modal-overlay">
    <div class="modal-content2">
      <button @click="closeFollow" class="close-follow inside-modal">X</button>
      <div class="follow-section">
        <div class="follow-list">
          <p class="follow-title">팔로잉</p>
          <ul>
            <li 
            v-for="user in props.userData.followings" 
            :key="user.id"
            @click="goDetail(user.username)"
            class="follow-item follow-link"
            >
              {{ user.nickname }} (ID: {{ user.username }})
            </li>
          </ul>
        </div>
        <div class="follow-list">
          <p class="follow-title">팔로워</p>
            <ul>
              <li 
              v-for="user in props.userData.followers" 
              :key="user.id"
              @click="goDetail(user.username)"
              class="follow-item follow-link"
              >
                {{ user.nickname }} (ID: {{ user.username }})
              </li>
            </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- 좋아요한 뮤비 modal -->
  <div v-if="isMovieLike" class="modal-overlay">
    <div class="modal-content2">
      <button @click="closeMyMovie" class="close-follow inside-modal">X</button>
      <div class="follow-section">
        <div class="follow-list">
          <p class="follow-title">좋아요한 영화</p>
          <ul>
            <li v-for = "movie in props.userData.like_movies"
            :key ="movie.id"
            @click="goMovie(movie.id)"
            class="follow-item follow-link"
            >
              {{movie.title}}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { useMovieStore } from '@/stores/counter'
import axios from 'axios'
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  userData: Object
})

// 프로필 옵션들
const profileOptions = [
  { value: "profile_images/profile1.jpg", src: new URL('@/assets/profile_images/profile1.jpg', import.meta.url).href, label: "Image 1" },
  { value: "profile_images/profile2.jpg", src: new URL('@/assets/profile_images/profile2.jpg', import.meta.url).href, label: "Image 2" },
  { value: "profile_images/profile3.jpg", src: new URL('@/assets/profile_images/profile3.jpg', import.meta.url).href, label: "Image 3" },
  { value: "profile_images/profile4.jpg", src: new URL('@/assets/profile_images/profile4.jpg', import.meta.url).href, label: "Image 4" },
  { value: "profile_images/profile5.jpg", src: new URL('@/assets/profile_images/profile5.jpg', import.meta.url).href, label: "Image 5" },
  { value: "profile_images/profile6.jpg", src: new URL('@/assets/profile_images/profile6.jpg', import.meta.url).href, label: "Image 6" },
  { value: "profile_images/default_profile.jpg", src: new URL('@/assets/profile_images/default_profile.jpg', import.meta.url).href, label: "Image 7" }
]

// 상태 변수
const profile_image = ref('')
const showModal = ref(false)
const nickname = ref('')
const route = useRoute()
const router = useRouter()
const store = useMovieStore()
const userId = ref(route.params.user_id) 
const userData = ref({})
const isFollowing = ref(false)
const followModal = ref(false)
// 내 페이지인지 확인하는 변수
// const isMyPage = ref(false)
const isNotMyPage = computed(() => !isMyPage.value)
const localUserData = ref({ ...props.userData });

// 내 페이지인지 확인하는 computed 속성
const isMyPage = computed(() => String(store.userId) === String(userId.value))
// 사용자 데이터 불러오기 함수
const fetchUserData = (id) => {
  if (store.token) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${id}/mypage/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then((res) => {
        userData.value = res.data
        nickname.value = res.data.nickname // 닉네임 초기화
        profile_image.value = res.data.profile_image // 프로필 이미지 초기화
      })
      .catch((err) => {
        console.error('유저 정보를 불러오는 중 오류 발생:', err)
      })

    // 팔로우 상태 확인
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${id}/follow/`,
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
      })
  }
}

// 마운트될 때와 라우트 변경 시 사용자 정보 불러오기
onMounted(() => {
  fetchUserData(userId.value)
  console.log('팔로잉',props.userData.followings)
  console.log('팔로워',props.userData.followers)
})

// 라우트 변경 시 업데이트
watch(() => route.params.user_id, (newUserId) => {
  userId.value = newUserId
  fetchUserData(userId.value)
})
watch(() => props.userData, (newValue) => {
  localUserData.value = { ...newValue };
});

// 회원 정보 수정
const updateData = () => {
  if (!store.token) {
    alert('로그인이 필요합니다')
    return
  }
  axios({
    method: 'put',
    url: `http://127.0.0.1:8000/accounts/${userId.value}/update/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      nickname: nickname.value,
      profile_image: profile_image.value
    }
  })
    .then((res) => {
      userData.value = {
        ...userData.value, // 기존 데이터 유지
        ...res.data // 응답으로 온 데이터 덮어쓰기
      }
      alert('회원정보가 성공적으로 수정되었습니다')
      showModal.value = false // 모달 닫기
      router.go(0)
    })
    .catch((err) => {
      console.error('회원정보 수정 중 오류:', err)
      alert('회원정보 수정에 실패했습니다')
    })
}

// 팔로우/언팔로우 기능
const toggleFollow = () => {
  if (!store.token) {
    alert('로그인이 필요합니다')
    return
  }

  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/accounts/${userId.value}/follow/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((res) => {
  if (res.data.message === '팔로우') {
    isFollowing.value = true;
    localUserData.value = {
      ...localUserData.value, // 기존 데이터 복사
      followers_count: localUserData.value.followers_count + 1, // 변경된 값
    };
  } else if (res.data.message === '언팔로우') {
    isFollowing.value = false;
    localUserData.value = {
      ...localUserData.value,
      followers_count: localUserData.value.followers_count - 1, // 변경된 값
    };
  }
})

    .catch((err) => {
      console.error('팔로우/언팔로우 요청 중 오류 발생:', err)
    })
}

// 모달 관련 상태 변수와 함수
const showDeleteModal = ref(false)
const password = ref('')
const oldPassword = ref('')
const newPassword1 = ref('')
const newPassword2 = ref('')
const showPasswordChange = ref(false)

const openDeleteModal = () => {
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  password.value = ''
}

const closePasswordModal = () => {
  showPasswordChange.value = false
  oldPassword.value = ''
  newPassword1.value = ''
  newPassword2.value = ''
}

const closeFollow = () => {
  followModal.value= false
}
const isMovieLike = ref(false)
const closeMyMovie = () => {
  isMovieLike.value = false
}

// 비밀번호 변경
const changePassword = () => {
  if (newPassword1.value !== newPassword2.value) {
    alert('새 비밀번호가 일치하지 않습니다. 다시 확인해주세요.');
    return;
  }
  axios({
    method: 'put',
    url: `http://127.0.0.1:8000/accounts/password/change/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      oldPassword: oldPassword.value,
      newPassword1: newPassword1.value,
      newPassword2: newPassword2.value
    }
  })
    .then((res) => {
      console.log(res)
      alert('비밀번호가 성공적으로 변경되었습니다')
      closePasswordModal()
    })
    .catch((err) => {
      if (err.response && err.response.status === 400) {
        alert(err.response.data.message)
      }
      console.log(err)
      alert('비밀번호 변경 중 오류가 발생했습니다.')
    })
}

// 회원탈퇴
const userDelete = () => {
  axios({
    method: 'delete',
    url: `http://127.0.0.1:8000/accounts/delete/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      password: password.value
    }
  })
    .then(() => {
      alert('회원탈퇴가 완료되었습니다')
      store.logout2()
      
    })
    .catch((err) => {
      console.log(err)
      alert(err.response.data.message)
    })
}

// 다이어리 공개/비공개 여부
const isPublicDiary = () => {
  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/accounts/${userId.value}/public/`,
    headers: {
       Authorization: `Token ${store.token}`
    }
  }).then((res) => {
    userData.value.is_public = res.data.is_public
    alert(res.data.message)
  }).catch((err) => {
    console.err('공개 상태 변경 중 오류 발생:', err)
    alert('공개 상태 변경에 실패했습니다.')
  })
}

const goDetail = (user_username) => {
  router.push({name : 'MyPageView', params:{user_id: user_username}})
}
const goMovie = (movie_id) => {
  router.push({name:'detail', params:{movie_id:movie_id}})
}
</script>




<style scoped>
.followBtn {
  /* margin-left: 15px; */
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
  font-family: "Noto Sans KR", sans-serif;
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
  font-family: "Noto Sans KR", sans-serif;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 380px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
}



.modal-actions {
  margin-top: 20px;
  display: flex;

}

.modal-actions button {
  padding: 8px 12px;
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

.new-form-input {
  width: 80%;
  padding: 15px;
  font-size: 1rem;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafafa;
}

.public-btn {
  margin: 3px;
  padding: 5px;
  font-family: "Noto Sans KR", sans-serif;
  margin-left: 10px;
  background-color: #f857a7;
  font-size: 1rem;
}
.public-btn2{
  padding: 5px;
  margin-left: 10px;
  background-color: white;
  font-size: 1.5rem;
  margin: 0;
}

.public-btn:hover {
  background-color: #ff007f;

}
.public-btn2:hover {
  background-color: white;

}

.close-follow.inside-modal {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #333;
}

.modal-content2 {
  font-family: "Noto Sans KR", sans-serif;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  border: 2px solid #e599d2;
  width: 500px;
  box-shadow: 10px 10px 0 #f4619e;
  position: relative;
}
.follow-section {
  display: flex;
  gap: 30px;
  justify-content: center;
}

.follow-list {
  padding: 10px 0;
}

.follow-title {
  font-weight: bold;
  margin-bottom: 10px;
  font-size: 18px;
}

.follow-item {
  padding: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.follow-item:hover {
  background-color: #f0f0f0;
}

.follow-link {
  color: #333;
  /* text-decoration: underline; */
}

.follow-link:hover {
  text-decoration: none;
  color: black;
}

.follow-hover {
  cursor: pointer;
  transition: color 0.3s ease;
}

.follow-hover:hover {
  color: #ff398b;
}
</style>
