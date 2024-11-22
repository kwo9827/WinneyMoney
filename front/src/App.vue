<template>
  <header>
    <nav class="nav-container">
      <div class="nav-center">
        <RouterLink :to="{ name: 'HomeView' }" class="logo">
          <span class="logo-text">WinneyMoney</span>
        </RouterLink>
      </div>
      <div class="nav-left">
        <RouterLink :to="{ name: 'FinanceView' }" class="nav-item">예/적금 상품목록</RouterLink>
        <RouterLink :to="{ name: 'ArticleView' }" class="nav-item">유저 게시판</RouterLink>
        <RouterLink :to="{ name: 'NewsHomeView' }" class="nav-item">뉴스</RouterLink>
        <RouterLink :to="{ name: 'ExchangeView' }" class="nav-item">환전 하기</RouterLink>
        <RouterLink :to="{ name: 'MapView' }" class="nav-item">지도 보기</RouterLink>
      </div>
      <div class="nav-right">
        <template v-if="store.isLogin">
          <div class="profile-container" @click="toggleDropdown">
            <!-- 프로필 이미지 -->
            <img class="profile-img" src="https://via.placeholder.com/40" alt="프로필 이미지" />
            <span class="username">{{ store.username }}</span>
            <!-- 드롭 다운 메뉴 -->
            <div v-if="dropdownVisible" class="dropdown-menu">
              <RouterLink :to="{ name: 'ProfileView' }">내 프로필</RouterLink>
              <RouterLink :to="{ name: 'EditProfileView' }">회원정보 변경</RouterLink>
              <a href="#" @click.prevent="logOut">로그아웃</a>
              <a href="#" @click.prevent="confirmDeleteAccount">회원탈퇴</a>
            </div>
          </div>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'LogInView' }" class="auth-link">로그인</RouterLink>
          <RouterLink :to="{ name: 'SignUpView' }" class="auth-link">회원가입</RouterLink>
        </template>
      </div>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const store = useAccountStore()

const dropdownVisible = ref(false)

const toggleDropdown = () => {
  dropdownVisible.value = !dropdownVisible.value
}

const logOut = () => {
  store.logOut()
}

const confirmDeleteAccount = () => {
  if (window.confirm('정말로 회원탈퇴를 진행하시겠습니까?')) {
    store.deleteAccount()
  }
}
</script>

<style scoped>
.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8f9fa;
}

.nav-left, .nav-right {
  display: flex;
  gap: 1rem;
}

a {
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
}

a:hover {
  color: #0056b3;
}

.profile-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.username {
  font-weight: bold;
  color: #007bff;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 1000;
}

.dropdown-menu p, 
.dropdown-menu a {
  color: black;
  text-decoration: none;
  cursor: pointer;
  margin: 0;
  font-weight: normal; /* 글자를 기본 두께로 설정 */
}

.dropdown-menu p:hover, 
.dropdown-menu a:hover {
  color: #0056b3; /* 글씨 색상 */
  font-weight: bold; /* 글씨 진하게  */
}
</style>
