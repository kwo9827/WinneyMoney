<template>
  <h1>적금</h1>
  <div>
    <div class="container mt-5">
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAccountStore } from '@/stores/accounts';
import { useFinanceStore } from '@/stores/finance';
import axios from 'axios';
import SavingListItem from './SavingListItem.vue';

// 예금 데이터 및 필터 상태
const savings = ref([]); // 반드시 빈 배열로 초기화
const bank = ref('');
const selectedPeriod = ref('');
const periods = [6, 12, 24, 36];

const store = useAccountStore();
const financeStore = useFinanceStore();
const API_URL = store.API_URL;

// API 호출 및 데이터 로드
onMounted(() => {
  axios.get(`${API_URL}/finlife/saving-products/`) // API 엔드포인트
    .then(res => {
      console.log('API 응답:', res.data);
      financeStore.getSavings(res.data); // API 응답 데이터를 저장
    }).then(() => {
      savings.value = financeStore.savings;
    })
    .catch(err => {
      console.error('API 호출 오류:', err);
    });
});

// 필터링된 예금 리스트
const filteredSavings = computed(() => {
  return savings.value.filter(saving => {
    // 은행명 필터
    const bankFilter = saving.kor_co_nm.toLowerCase().includes(bank.value.toLowerCase());
    // 기간 필터
    const periodFilter = !selectedPeriod.value || saving.options.some(option => option.save_trm === parseInt(selectedPeriod.value));
    return bankFilter && periodFilter;
  });
});

// 기간별 정렬
const sortByPeriod = (period) => {
  filteredSavings.value.sort((a, b) => {
    const aOption = a.options.find(option => option.save_trm === period);
    const bOption = b.options.find(option => option.save_trm === period);
    const aRate = aOption ? aOption.intr_rate : 0; // 해당 기간 금리가 없으면 0
    const bRate = bOption ? bOption.intr_rate : 0; // 해당 기간 금리가 없으면 0
    return bRate - aRate; // 내림차순 정렬
  });
};
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  font-weight: bold;
  background-color: #3498db;
  color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.header-item {
  flex: 1;
  text-align: center;
  font-size: 1rem;
  cursor: pointer;
}

.filters {
  margin-bottom: 1rem;
}

.filters button,
.filters input,
.filters select {
  margin-left: 0.5rem;
  margin-right: 1rem;
  padding: 0.5rem;
  font-size: 1rem;
}
</style>
