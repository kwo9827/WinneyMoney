<template>
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

const props = defineProps({
  deposits: Array, // 현재 페이지의 예금 데이터
  periods: Array, // 기간 배열
});

const router = useRouter();
const goToDetail = (id) => {
  router.push({ name: 'DepositDetailView', params: { product_id: id } });
};
</script>

<style scoped>
.deposit-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
</style>
