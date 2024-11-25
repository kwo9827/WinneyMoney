<template>
  <div class="favorite-savings-container">
    <h2 class="title">내가 가입한 적금 상품</h2>

    <!-- 데이터 로딩 중 메시지 -->
    <div v-if="isLoading" class="loading-message">
      데이터를 불러오는 중입니다...
    </div>

    <!-- 적금 목록 -->
    <ul v-if="savings.length" class="saving-list">
      <li v-for="saving in savings" :key="saving.id" class="saving-item">
        <div class="saving-info">
          <h3>{{ saving.kor_co_nm }} - {{ saving.fin_prdt_nm }}</h3>
          <p>가입 방법: {{ saving.join_way }}</p>
          <p>최고 한도: {{ saving.max_limit === -1 ? '제한 없음' : saving.max_limit + '원' }}</p>
          <p>만기 후 이자율: {{ saving.mtrt_int }}</p>
        </div>
        <button class="remove-button" @click="removeSaving(saving.fin_prdt_cd)">
          삭제
        </button>
      </li>
    </ul>

    <!-- 적금 목록이 없을 때 메시지 -->
    <div v-else-if="!isLoading" class="empty-message">
      가입된 적금 상품이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useFinanceStore } from '@/stores/finance';

// Pinia 스토어 사용
const financeStore = useFinanceStore();

// 상태 관리
const isLoading = ref(false);

// 적금 목록 가져오기
const savings = computed(() => financeStore.favoriteSavings);

// 데이터 가져오기
const fetchFavorites = async () => {
  isLoading.value = true;
  try {
    await financeStore.fetchFavorites(); // 즐겨찾기 데이터 최신화
  } catch (error) {
    console.error('즐겨찾기 데이터 가져오기 실패:', error);
  } finally {
    isLoading.value = false;
  }
};

// 적금 상품 삭제
const removeSaving = async (fin_prdt_cd) => {
  try {
    await financeStore.toggleFavoriteSaving(fin_prdt_cd); // 스토어 상태 업데이트
    console.log('적금 상품 삭제 성공:', fin_prdt_cd);
  } catch (error) {
    console.error('적금 상품 삭제 실패:', error);
  }
};

// 컴포넌트 로드 시 데이터 가져오기
onMounted(() => {
  fetchFavorites();
});
</script>

<style scoped>
.favorite-savings-container {
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 2rem auto;
}

.title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #2c3e50;
}

.saving-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.saving-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  border: 1px solid #ecf0f1;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.saving-info h3 {
  margin: 0 0 0.5rem 0;
  color: #3498db;
  font-size: 1.2rem;
}

.saving-info p {
  margin: 0.25rem 0;
  color: #34495e;
  font-size: 0.9rem;
}

.remove-button {
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.remove-button:hover {
  background-color: #c0392b;
}

.loading-message {
  text-align: center;
  color: #7f8c8d;
  font-size: 1rem;
}

.empty-message {
  text-align: center;
  color: #7f8c8d;
  font-size: 1rem;
  margin-top: 1rem;
}
</style>
