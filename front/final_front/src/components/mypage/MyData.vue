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
        <p>방문자 수: {{ userData.visit_count }}</p>
        <p>모은 조약돌 수: {{ userData.stone }}</p>
      </div>
    </div>
    <div class="actions" v-if="userId == store.userId">
      <RouterLink to="/main"><button>회원정보 수정</button></RouterLink>
      <RouterLink to="/main"><button>비밀번호 수정</button></RouterLink>
      <button>회원 탈퇴</button>
    </div>
  </div>


  <!-- 회원정보수정 Modal -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h3>회원 정보 수정</h3>
      <div class="input-group">
        <label for=""></label>
      </div>
    </div>
  </div>


</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { RouterLink } from 'vue-router';

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
</style>
