<template>
  <div class="finance-container">
    <!-- 네비게이션 바 -->
    <nav class="nav-bar">
      <RouterLink
        :to="{ name: 'DepositView' }"
        class="nav-link"
        :class="{ active: $route.name === 'DepositView' }"
      >
        예금
      </RouterLink>
      <RouterLink
        :to="{ name: 'SavingView' }"
        class="nav-link"
        :class="{ active: $route.name === 'SavingView' }"
      >
        적금
      </RouterLink>
    </nav>

    <!-- 메인 컨텐츠 -->
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.finance-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f4f6f8;
}

/* 네비게이션 바 스타일 */
.nav-bar {
  padding: 1rem 2rem;
  background-color: #3498db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* 네비게이션 링크 스타일 */
.nav-link {
  color: #ffffff;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0 1.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.3s, transform 0.2s;
}

.nav-link:hover {
  background-color: #2980b9;
  transform: scale(1.1);
}

/* 현재 활성화된 페이지 스타일 */
.nav-link.active {
  background-color: #1f618d;
  color: #ffffff;
}

/* 메인 컨텐츠 영역 스타일 */
.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 1rem;
  margin: 1rem auto;
  max-width: 1200px;
}
</style>
