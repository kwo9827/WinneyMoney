<template>
<<<<<<< HEAD
  <div class="data-row">
    <!-- 클릭하여 상세 페이지로 이동 -->
    <div @click="goToDetail" class="deposit-item">
      <p>{{ deposit.id }}</p>
    </div>
    <!-- 은행명 -->
    <span class="data-item">{{ deposit.kor_co_nm }}</span>
    <!-- 상품명 -->
    <span class="data-item">{{ deposit.fin_prdt_nm }}</span>
    <!-- 금리 -->
    <span
      v-for="(rate, period) in rates"
      :key="'rate-' + period"
      class="data-item"
      :class="{ highlight: period === highlightPeriod }"
    >
      <span v-if="rate">{{ rate }}%</span>
      <span v-else>-</span>
    </span>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
=======
  <table class="deposit-table">
    <!-- 테이블 헤더 -->
    <thead>
      <tr>
        <th>은행명</th>
        <th>상품명</th>
        <th v-for="period in periods" :key="'header-' + period">
          {{ period }}개월
        </th>
      </tr>
    </thead>
    <!-- 테이블 본문 -->
    <tbody>
      <tr
        v-for="deposit in deposits"
        :key="deposit.id"
        @click="goToDetail(deposit.id)"
        class="data-row"
      >
        <td>{{ deposit.kor_co_nm }}</td>
        <td>{{ deposit.fin_prdt_nm }}</td>
        <td
          v-for="period in periods"
          :key="'data-' + period"
          class="interest-rate"
        >
          <span
            v-if="deposit.options.find(option => option.save_trm === period)?.intr_rate"
          >
            {{
              deposit.options.find(option => option.save_trm === period)
                .intr_rate
            }}%
          </span>
          <span v-else>-</span>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { useRouter } from 'vue-router';
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc

const props = defineProps({
  deposits: Array,
  periods: Array,
});

const router = useRouter();
<<<<<<< HEAD

// 기간별 금리 계산
const rates = computed(() => {
  const periods = [6, 12, 24, 36];
  return periods.reduce((acc, period) => {
    const option = props.deposit?.options?.find((opt) => opt.save_trm === period);
    acc[period] = option?.intr_rate || null; // 금리가 없으면 null
    return acc;
  }, {});
});

// 상세 페이지로 이동
const goToDetail = () => {
  if (props.deposit?.id) {
    router.push(`/finance/deposit/${props.deposit.id}`);
  } else {
    console.warn("Invalid deposit data:", props.deposit);
  }
=======
const goToDetail = (id) => {
  router.push({ name: 'DepositDetailView', params: { product_id: id } });
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc
};
</script>

<style scoped>
<<<<<<< HEAD
.data-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  background-color: white;
  cursor: pointer;
=======
.deposit-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc
}

.deposit-table th,
.deposit-table td {
  padding: 1rem;
  text-align: center;
  font-size: 1rem;
  border: 1px solid #dee2e6;
}

.deposit-table th {
  background-color: #3498db;
  color: white;
  font-weight: bold;
}

.deposit-table td {
  background-color: #ffffff;
  color: #34495e;
}

.data-row {
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.data-row:hover {
  background-color: #f1f8ff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.interest-rate {
  font-weight: bold;
  color: #27ae60;
}
<<<<<<< HEAD

.highlight {
  background-color: #dccb87;
  font-weight: bold;
  border-radius: 0.3rem;
  padding: 0.2rem 0.5rem;
}

.deposit-item p {
  margin: 0;
  font-size: 0.9rem;
  color: #7f8c8d;
}
=======
>>>>>>> 49a65e57698ee39bd963daff82bd4284ff1195dc
</style>
