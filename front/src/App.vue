<template>
  <v-app> <!-- Vuetify의 최상위 컴포넌트 -->
    <v-app-bar app>
      <v-container class="nav-container">
        <!-- 로고 -->
        <RouterLink :to="{ name: 'HomeView' }" class="logo">
          <span class="logo-text">WinneyMoney</span>
        </RouterLink>
<<<<<<< HEAD
      </div>
      <div class="nav-left">
        <RouterLink :to="{ name: 'FinanceView' }" class="nav-item">예/적금 상품목록</RouterLink>
        <RouterLink :to="{ name: 'PortfolioCreateView' }" class="nav-item">포트폴리오 생성</RouterLink>
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
=======

        <!-- 왼쪽 네비게이션 -->
        <v-row class="nav-left">
          <v-btn text :to="{ name: 'FinanceView' }">예/적금 상품목록</v-btn>
          <v-btn text :to="{ name: 'ArticleView' }">유저 게시판</v-btn>
          <v-btn text :to="{ name: 'NewsHomeView' }">뉴스</v-btn>
          <v-btn text :to="{ name: 'ExchangeView' }">환전 하기</v-btn>
          <v-btn text :to="{ name: 'MapView' }">지도 보기</v-btn>
        </v-row>

        <!-- 오른쪽 네비게이션 -->
        <v-row class="nav-right">
          <template v-if="store.isLogin">
            <!-- 드롭다운 프로필 -->
            <v-menu offset-y>
              <template #activator="{ props }">
                <div class="profile-container" v-bind="props">
                  <img class="profile-img" src="https://via.placeholder.com/40" alt="프로필 이미지" />
                  <span class="username">{{ store.username }}</span>
                </div>
              </template>
              <v-list>
                <v-list-item :to="{ name: 'ProfileView' }" link>
                  <v-list-item-title>내 프로필</v-list-item-title>
                </v-list-item>
                <v-list-item :to="{ name: 'EditProfileView' }" link>
                  <v-list-item-title>회원정보 변경</v-list-item-title>
                </v-list-item>
                <v-list-item @click="logOut">
                  <v-list-item-title>로그아웃</v-list-item-title>
                </v-list-item>
                <v-list-item @click="confirmDeleteAccount">
                  <v-list-item-title>회원탈퇴</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
          <template v-else>
            <v-btn text :to="{ name: 'LogInView' }">로그인</v-btn>
            <v-btn text :to="{ name: 'SignUpView' }">회원가입</v-btn>
          </template>
        </v-row>
      </v-container>
    </v-app-bar>
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc
</template>

<script setup>
import { ref } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const store = useAccountStore()

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
}

.profile-container {
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

.v-btn {
  text-transform: none; /* 버튼 텍스트 대문자 방지 */
}
</style>
