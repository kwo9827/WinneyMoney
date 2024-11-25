<template>
  <div class="favorites-container">
    <!-- 네비게이션 -->
    <nav class="favorites-nav">
      <button
        :class="{ active: activeTab === 'deposits' }"
        @click="activeTab = 'deposits'"
      >
        예금 가입 목록
      </button>
      <button
        :class="{ active: activeTab === 'savings' }"
        @click="activeTab = 'savings'"
      >
        적금 가입 목록
      </button>
    </nav>

    <!-- 조건부 렌더링 -->
    <div>
      <FavoriteDeposits v-if="activeTab === 'deposits'" />
      <FavoriteSavings v-if="activeTab === 'savings'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import FavoriteDeposits from "@/components/Finlife/FavoriteDeposits.vue";
import FavoriteSavings from "@/components/Finlife/FavoriteSavings.vue";

const activeTab = ref("deposits"); // 기본적으로 예금 탭 활성화
</script>

<style scoped>
.favorites-container {
  padding: 2rem;
}

.favorites-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 1rem;
}

button.active {
  background-color: #3498db;
  color: white;
}

button:not(.active) {
  background-color: #ecf0f1;
  color: #7f8c8d;
}

button:hover {
  background-color: #2980b9;
  color: white;
}
</style>
