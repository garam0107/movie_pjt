<template>
  <div class="mydata-container">
    <div class="profile-header">
      <div class="profile-image">
        <!-- <img :src="`@/assets/${props.userData.profile_image}`" alt="프로필 이미지"> -->
        <img src="@/assets/default_profile.jpg" alt="profile_img">
      </div>
      <div class="user-info">
        <h2>{{ props.userData.nickname }}</h2>
        <p>{{ props.userData.email }}</p>
        <!-- <p>팔로워 {{ props.userData.followers }} | 팔로잉 {{ props.userData.following }}</p> -->
      </div>
    </div>
    <div class="user-stats">
      <div class="stat">
        <h3>28개</h3>
        <p>평가</p>
      </div>

    </div>
    <div class="actions">
      <button>회원 탈퇴</button>
      <RouterLink><button>회원정보 수정</button></RouterLink>
      <RouterLink><button>비밀번호 수정</button></RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';

const props = defineProps ({
  userData: Object
})
</script>

<style scoped>
.mydata-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-image img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
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

.stat h3 {
  font-size: 2rem;
  margin: 0;
  color: gray;
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