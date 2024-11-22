<template>
<<<<<<< HEAD
  <div>
    <div class="container">
      <!-- 데이터 로딩 메시지 -->
      <div v-if="loading">
        <p>데이터를 로드 중입니다...</p>
      </div>
      <!-- 데이터가 로드된 후 -->
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
          <button @click="resetOrder">정렬 초기화</button>
          <hr />
        </div>
        <!-- DepositListItem 컴포넌트 -->
        <div v-for="deposit in filteredDeposits" :key="deposit.id">
          <DepositListItem
            :deposit="deposit"
            :highlight-period="selectedPeriod"
          />
        </div>
      </div>
=======
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
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFinanceStore } from '@/stores/finance';
import DepositListItem from './DepositListItem.vue';

<<<<<<< HEAD
// 로컬 상태 및 스토어
const loading = ref(true); // 로딩 상태
const deposits = ref([]);
const initialDeposits = ref([]);
const financeStore = useFinanceStore();
const bank = ref(''); // 은행명 필터
const selectedPeriod = ref(0); // 기간 필터
const periods = [6, 12, 24, 36]; // 기간 옵션

// 데이터 로드
onMounted(async () => {
  loading.value = true; // 로딩 시작
  await financeStore.fetchDeposits(); // 스토어에서 데이터 로드
  deposits.value = [...financeStore.deposits] || []; // 로컬로 데이터 복사
  initialDeposits.value = [...financeStore.deposits] || [];
  loading.value = false; // 로딩 종료
});

// 정렬 초기화
const resetOrder = () => {
  deposits.value = [...initialDeposits.value]; // 초기 데이터로 복원
};
=======
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
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc

const filteredDeposits = computed(() => {
  return deposits.value.filter((deposit) => {
<<<<<<< HEAD
    // 은행명 필터
    const bankFilter = deposit.kor_co_nm
      .toLowerCase()
      .includes(bank.value.toLowerCase());
    // 기간 필터
=======
    const bankFilter = deposit.kor_co_nm
      .toLowerCase()
      .includes(bank.value.toLowerCase());
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc
    const periodFilter =
      !selectedPeriod.value ||
      deposit.options.some(
        (option) => option.save_trm === Number(selectedPeriod.value)
      );
    return bankFilter && periodFilter;
<<<<<<< HEAD
  });
});

// 기간별 정렬
const sortByPeriod = (period) => {
  deposits.value.sort((a, b) => {
    const aOption = a.options.find((option) => option.save_trm === period);
    const bOption = b.options.find((option) => option.save_trm === period);
    const aRate = aOption ? aOption.intr_rate : 0; // 해당 기간 금리가 없으면 0
    const bRate = bOption ? bOption.intr_rate : 0; // 해당 기간 금리가 없으면 0
    return bRate - aRate; // 내림차순 정렬
=======
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc
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
