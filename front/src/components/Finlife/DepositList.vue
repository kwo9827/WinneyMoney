<template>
  <div>
    <div class="container">
      <!-- 데이터가 없을 때 로딩 메시지 -->
      <div v-if="!financeStore.deposits.length">
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
          <button id="count">{{ filteredDeposits.length }}</button>
          <hr />
        </div>
        <!-- DepositListItem 컴포넌트 -->
        <div v-for="deposit in filteredDeposits" :key="deposit.id">
          <DepositListItem :deposit="deposit" :highlight-period="selectedPeriod" />
        </div>
      </div>
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
const deposits = computed(() => {
  return financeStore.deposits
})
const bank = ref('')
const selectedPeriod = ref(0)
const periods = [6, 12, 24, 36]

// 데이터 로드
onMounted(async () => {
  await financeStore.fetchDeposits() // 스토어에서 데이터 로드
  deposits.value = [...financeStore.deposits] || []// 로컬로 데이터 복사
})

// 필터링된 예금 리스트
const filteredDeposits = computed(() => {
  return deposits.value.filter(deposit => {
    // 은행명 필터
    const bankFilter = deposit.kor_co_nm.toLowerCase().includes(bank.value.toLowerCase())
    // 기간 필터
    const periodFilter = !selectedPeriod.value || deposit.options.some(option => option.save_trm === Number(selectedPeriod.value))
    return bankFilter && periodFilter
  })
})

// 기간별 정렬
const sortByPeriod = (period) => {
  deposits.value.sort((a, b) => {
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
