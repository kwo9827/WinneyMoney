<template>
  <div id="app">
    <!-- 네비게이션 바 -->
    <header class="navbar">
      <div class="nav-container">
        <!-- 로고 -->
        <div class="logo">
          <RouterLink :to="{ name: 'HomeView' }">WinneyMoney</RouterLink>
        </div>

        <!-- 네비게이션 메뉴 -->
        <nav class="nav-links">
          <RouterLink :to="{ name: 'FinanceView' }" class="nav-item">예/적금 상품목록</RouterLink>
          <RouterLink :to="{ name: 'ArticleView' }" class="nav-item">유저 게시판</RouterLink>
          <RouterLink :to="{ name: 'PortfolioCreateView' }" class="nav-item">포트폴리오 만들기</RouterLink>
          <RouterLink :to="{ name: 'NewsHomeView' }" class="nav-item">뉴스</RouterLink>
          <RouterLink :to="{ name: 'ExchangeView' }" class="nav-item">환전 하기</RouterLink>
          <RouterLink :to="{ name: 'MapView' }" class="nav-item">지도 보기</RouterLink>
        </nav>

        <!-- 사용자 메뉴 -->
        <div class="user-menu">
          <template v-if="store.isLogin">
            <div class="profile" @click="toggleDropdown">
              <img src="https://via.placeholder.com/40" alt="프로필" class="profile-img" />
              <span>{{ store.username }}</span>
            </div>
            <ul v-if="dropdownOpen" class="dropdown-menu">
              <li><RouterLink :to="{ name: 'ProfileView' }">내 프로필</RouterLink></li>
              <li><RouterLink :to="{ name: 'FavoritesView' }">가입 목록</RouterLink></li>
              <li><RouterLink :to="{ name: 'EditProfileView' }">회원정보 변경</RouterLink></li>
              <li @click="logOut">로그아웃</li>
              <li @click="confirmDeleteAccount">회원탈퇴</li>
            </ul>
          </template>
          <template v-else>
            <RouterLink :to="{ name: 'LogInView' }" class="nav-item">로그인</RouterLink>
            <RouterLink :to="{ name: 'SignUpView' }" class="nav-item">회원가입</RouterLink>
          </template>
        </div>
      </div>
    </header>

    <!-- 메인 컨텐츠 -->
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/accounts";

const store = useAccountStore();
const dropdownOpen = ref(false);

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
  console.log("드롭다운 상태:", dropdownOpen.value); // 상태 변화 확인
};


const logOut = () => {
  store.logOut();
};

const confirmDeleteAccount = () => {
  if (confirm("정말로 회원탈퇴를 진행하시겠습니까?")) {
    store.deleteAccount();
  }
};
</script>

<style scoped>
/* 전체 앱 스타일 */
#app {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 네비게이션 바 스타일 */
.navbar {
  background-color: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
}

.logo a {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
}

.nav-item:hover {
  text-decoration: underline;
}

/* 사용자 메뉴 */
.user-menu {
  display: flex;
  align-items: center;
  position: relative;
}

.profile {
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

.dropdown-menu {
  display: block; /* 기본적으로 block 설정 */
  position: absolute;
  top: calc(100% + 10px); /* 상단에서 약간 띄움 */
  right: 0;
  background-color: #ffffff; /* 흰색 배경 */
  color: #333333; /* 텍스트 색상 */
  list-style: none;
  padding: 0.75rem 0; /* 메뉴 아이템 간격 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 더 부드러운 그림자 */
  border-radius: 0.75rem; /* 둥근 모서리 */
  z-index: 9999; /* 다른 요소 위에 표시 */
  min-width: 180px; /* 최소 너비 설정 */
}

.dropdown-menu li {
  padding: 0.5rem 1rem; /* 내부 여백 */
  cursor: pointer;
  font-size: 1rem; /* 글씨 크기 */
  font-weight: 500; /* 중간 굵기 */
  color: #34495e; /* 텍스트 색상 */
  transition: background-color 0.2s, color 0.2s; /* 부드러운 효과 */
}

.dropdown-menu li:hover {
  background-color: #f8f9fa; /* 마우스 오버 시 배경색 변경 */
  color: #2c3e50; /* 마우스 오버 시 텍스트 색상 변경 */
  border-radius: 0.5rem; /* 호버 시 모서리 둥글게 */
}

.dropdown-menu li a {
  text-decoration: none; /* 링크의 밑줄 제거 */
  color: inherit; /* 부모 요소의 색상 상속 */
  display: block; /* 전체 영역 클릭 가능 */
  width: 100%;
}

/* 메인 컨텐츠 */
main {
  padding: 1rem;
}
</style>
