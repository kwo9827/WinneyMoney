<template>
  <div>
    <div class="container">
      <!-- 데이터가 없을 때 로딩 메시지 -->
      <div v-if="!financeStore.savings.length">
        <p>데이터를 로드 중입니다...</p>
      </div>
      <!-- 데이터가 있을 때 -->
      <div v-else>
        <!-- 테이블 헤더 -->
        <div class="table-header">
          <span class="header-item">은행명</span>
          <span class="header-item">상품명</span>
          <span
            v-for="period in periods"
            :key="'header-' + period"
            class="header-item"
            @dblclick="sortByPeriod(period)"
          >
            {{ period }}개월
          </span>
        </div>

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
          <label for="count">검색된 상품 수 : </label>
          <button id="count">{{ filteredSavings.length }}</button>
          <hr />
        </div>
        <!-- SavingListItem 컴포넌트 -->
        <div v-for="saving in filteredSavings" :key="saving.id">
          <SavingListItem :saving="saving" :highlight-period="selectedPeriod" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFinanceStore } from '@/stores/finance';
import SavingListItem from './SavingListItem.vue';

// 스토어 및 필터 상태
const savings = ref([])
const financeStore = useFinanceStore();
const bank = ref('');
const selectedPeriod = ref('');
const periods = [6, 12, 24, 36]; // 개월 수 정의

onMounted(async () => {
  await financeStore.fetchSavings() // 스토어에서 데이터 로드
  savings.value = [...financeStore.savings] || []// 로컬로 데이터 복사
})

// 필터링된 적금 리스트
const filteredSavings = computed(() => {
  return savings.value.filter((saving) => {
    const bankFilter = saving.kor_co_nm
      .toLowerCase()
      .includes(bank.value.toLowerCase());
    const periodFilter =
      !selectedPeriod.value ||
      saving.options.some(
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

/* 적금 테이블 스타일 */
.saving-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.saving-table th,
.saving-table td {
  padding: 1rem;
  text-align: center;
  font-size: 1rem;
  border: 1px solid #dee2e6;
}

.saving-table th {
  background-color: #3498db;
  color: white;
  font-weight: bold;
}

.saving-table td {
  background-color: #ffffff;
  color: #34495e;
}

/* 로딩 메시지 스타일 */
.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-top: 2rem;
}
</style>
