<template>
  <div class="not-found">
    <h1>404: 페이지를 찾을 수 없습니다</h1>
    <p>요청하신 페이지가 존재하지 않습니다. URL을 다시 확인해주세요.</p>
    <RouterLink to="/">홈으로 이동</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 50px;
}

.not-found h1 {
  font-size: 2rem;
  color: #e74c3c;
}

.not-found p {
  font-size: 1.2rem;
  margin: 20px 0;
}
</style>
