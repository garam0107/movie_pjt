<template>
  <div class="mydata-container">
    <div class="profile-header">
      <div class="profile-image">
        <img :src="`/src/assets/${userData.profile_image}`" alt="프로필 이미지">
      </div>
      <div class="user-info">
        <div style="display: flex;">
          <h2>{{ userData.nickname }}</h2>
          <form @submit.prevent="follow">
            <button v-if="isFollowing" @click="toggleFollow" class="followBtn unfollowBtn">언팔로우</button>
            <button v-else @click="toggleFollow" class="followBtn">팔로우</button>
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
    <div class="actions">
      <RouterLink to="/main"><button>회원정보 수정</button></RouterLink>
      <RouterLink to="/main"><button>비밀번호 수정</button></RouterLink>
      <button>회원 탈퇴</button>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { RouterLink } from 'vue-router';

const route = useRoute();
const userId = route.params.user_id; // URL에서 user_id를 가져옴
const store = useMovieStore();
const userData = ref({}); // 유저 정보를 담을 변수
const isFollowing = ref(false);

// 마운트될 때 사용자 정보 불러오기
onMounted(() => {
  if (store.token) {
    // 특정 사용자의 데이터 요청
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId}/mypage/`, // 특정 유저 정보 요청
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      console.log('유저 데이터:', res.data);
      userData.value = res.data; // 유저 데이터를 상태에 저장
    })
    .catch((err) => {
      console.error('유저 정보를 불러오는 중 오류 발생:', err);
    });
  } else {
    console.error('토큰이 없습니다. 로그인 후 다시 시도해주세요.');
  }

  // 팔로우 상태 확인
  if (store.token) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/${userId}/follow/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      isFollowing.value = res.data.following.some(user => user.id === userId);
    })
    .catch((err) => {
      console.error('팔로우 상태를 확인하는 중 오류 발생:', err);
    });
  }
});

// 팔로우/언팔로우 기능
const toggleFollow = () => {
  if (!store.token) {
    alert('로그인이 필요합니다.');
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
      isFollowing.value = true;
    } else if (res.data.message === '언팔로우') {
      isFollowing.value = false;
    }
    console.log(res.data.message);
  })
  .catch((err) => {
    console.error('팔로우/언팔로우 요청 중 오류 발생:', err);
  });
};

// // 프로필 이미지 경로 가져오기
// const getImagePath = (imageName) => {
//   if (imageName) {
//     return `/src/assets/profile_images/${imageName}`;
//   } else {
//     return '/src/assets/default_profile.jpg'; // 기본 프로필 이미지
//   }
// };
</script>

<style scoped>
.followBtn {
  padding: 5px;
  border-radius: 30%;
  background-color: dodgerblue;
}

.followBtn:hover {
  background-color: blue;
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
