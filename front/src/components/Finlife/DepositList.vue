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

    <!-- 정렬 버튼 -->
    <div class="sort-buttons">
      <span>정렬:</span>
      <button
        v-for="period in periods"
        :key="'sort-' + period"
        class="sort-button"
        @click="toggleSort(period)"
      >
        {{ period }}개월
        <span v-if="selectedSortPeriod === period">
          {{ sortOrder === 'asc' ? '▲' : '▼' }}
        </span>
      </button>
      
      <!-- 정렬 초기화 버튼 -->
      <button
        class="reset-button"
        @click="resetSort"
      >
        정렬 초기화
      </button>
    </div>

    <!-- 데이터가 없을 때 로딩 메시지 -->
    <div v-if="!filteredDeposits.length" class="loading-message">
      데이터를 로드 중입니다...
    </div>
    <!-- 데이터가 있을 때 -->
    <div v-else>
      <!-- 리스트 -->
      <DepositListItem
        :deposits="paginatedDeposits"
        :periods="periods"
      />

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button
          class="page-btn"
          :disabled="currentPage === 1"
          @click="currentPage--"
        >
          이전
        </button>
        <button
          v-for="page in totalPages"
          :key="page"
          class="page-btn"
          :class="{ active: currentPage === page }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
        <button
          class="page-btn"
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFinanceStore } from '@/stores/finance';
import DepositListItem from './DepositListItem.vue';

// 스토어 사용
const financeStore = useFinanceStore();

// 필터 상태
const deposits = ref([]);
const bank = ref('');
const selectedPeriod = ref('');
const periods = [6, 12, 24, 36]; // 개월 수 정의

// 페이지네이션 상태
const currentPage = ref(1);
const itemsPerPage = 10;

// 정렬 상태
const selectedSortPeriod = ref(null); // 정렬 중인 기간
const sortOrder = ref('asc'); // 현재 정렬 순서 (asc or desc)

// 데이터 로드
onMounted(async () => {
  await financeStore.fetchDeposits();
  deposits.value = [...financeStore.deposits] || [];
});

// 필터링된 데이터
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

// 정렬된 데이터
const sortedDeposits = computed(() => {
  if (!selectedSortPeriod.value) return filteredDeposits.value; // 정렬 조건이 없으면 필터링 데이터 반환
  return [...filteredDeposits.value].sort((a, b) => {
    const aRate = a.options.find(
      (option) => option.save_trm === selectedSortPeriod.value
    )?.intr_rate || 0;
    const bRate = b.options.find(
      (option) => option.save_trm === selectedSortPeriod.value
    )?.intr_rate || 0;

    return sortOrder.value === 'asc' ? aRate - bRate : bRate - aRate;
  });
});

// 페이지네이션 처리
const totalPages = computed(() =>
  Math.ceil(sortedDeposits.value.length / itemsPerPage)
);

const paginatedDeposits = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return sortedDeposits.value.slice(start, end);
});

// 정렬 토글
const toggleSort = (period) => {
  if (selectedSortPeriod.value === period) {
    // 동일한 기간이면 정렬 순서를 토글
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    // 새로운 기간을 선택하면 해당 기간으로 정렬
    selectedSortPeriod.value = period;
    sortOrder.value = 'asc'; // 초기 정렬 순서는 오름차순
  }
};

// 정렬 초기화
const resetSort = () => {
  selectedSortPeriod.value = null;  // 정렬된 기간 초기화
  sortOrder.value = 'asc';  // 정렬 순서를 기본값(오름차순)으로 초기화
};

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

/* 정렬 버튼 */
.sort-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 1rem;
}

.sort-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  cursor: pointer;
  background-color: #3498db;
  color: white;
}

.sort-button:hover {
  background-color: #1f618d;
}

/* 페이지네이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  gap: 0.5rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  cursor: pointer;
  background-color: white;
  color: #3498db;
}

.page-btn.active {
  background-color: #3498db;
  color: white;
}

.page-btn:disabled {
  background-color: #e0e0e0;
  color: #b0b0b0;
  cursor: not-allowed;
}

.reset-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  cursor: pointer;
  background-color: #e74c3c;
  color: white;
}

.reset-button:hover {
  background-color: #c0392b;
}
</style>
