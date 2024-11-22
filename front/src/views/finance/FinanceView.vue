<template>
  <div>
    <nav>
      <RouterLink :to="{ name: 'DepositView' }">예금</RouterLink>
      <RouterLink :to="{ name: 'SavingView' }">적금</RouterLink>
    </nav>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
/* 상단 네비게이션 스타일 */
nav {
  padding: 1rem;
  background-color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  top: 0;
  z-index: 1000;
  display: flex;
  justify-content: center;
}

nav a {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
  margin: 0 1rem;
  transition: color 0.2s ease-in-out;
}

nav a:hover {
  color: #1f618d;
}

/* 메인 콘텐츠 스타일 */
main {
  background-color: #fff;
}
</style>
