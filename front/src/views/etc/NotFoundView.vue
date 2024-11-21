<template>
  <div class="not-found">
    <h1>404 - 페이지를 찾을 수 없습니다.</h1>
    <RouterLink to="/">홈으로 돌아가기</RouterLink>
  </div>
</template>

<script setup></script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 20%;
  color: var(--text-color);
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: bold;
}
</style>
