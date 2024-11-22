<template>
  <div class="container">
    <!-- 필터 입력 -->
    <div class="filters">
      <label for="bank">은행명</label>
      <input
        type="text"
        id="bank"
        v-model="bank"
        placeholder="은행명을 입력하세요"
      />
      <label for="period">기간</label>
      <select id="period" v-model="selectedPeriod">
        <option value="">모든 기간</option>
        <option v-for="period in periods" :key="period" :value="period">
          {{ period }}개월
        </option>
      </select>
      <label for="count">검색된 상품 수:</label>
      <button id="count" class="count-button">{{ filteredDeposits.length }}</button>
    </div>

    <!-- 데이터가 없을 때 로딩 메시지 -->
    <div v-if="!filteredDeposits.length" class="loading-message">
      데이터를 로드 중입니다...
    </div>
    <!-- 데이터가 있을 때 -->
    <div v-else>
      <!-- 리스트 -->
      <DepositListItem
        :deposits="filteredDeposits"
        :periods="periods"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import DepositListItem from './DepositListItem.vue'

// 스토어 사용
const financeStore = useFinanceStore()

// 필터 상태
const deposits = ref([])
const bank = ref('')
const selectedPeriod = ref(0)
const periods = [6, 12, 24, 36]

// 데이터 로드
onMounted(async () => {
  await financeStore.fetchDeposits();
  deposits.value = [...financeStore.deposits] || [];
});

const filteredDeposits = computed(() => {
  return deposits.value.filter((deposit) => {
    const bankFilter = deposit.kor_co_nm
      .toLowerCase()
      .includes(bank.value.toLowerCase());
    const periodFilter =
      !selectedPeriod.value ||
      deposit.options.some(
        (option) => option.save_trm === Number(selectedPeriod.value)
      );
    return bankFilter && periodFilter;
  });
});
</script>

<style scoped>
.container {
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 필터 스타일 */
.filters {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1.5rem;
}

.filters input,
.filters select {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
}

.count-button {
  background-color: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 1rem;
}

.count-button:hover {
  background-color: #1f618d;
}

/* 로딩 메시지 */
.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-top: 2rem;
}
</style>
