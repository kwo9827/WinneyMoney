<template>
  <table class="saving-table">
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
        v-for="saving in savings"
        :key="saving.id"
        @click="goToDetail(saving.id)"
        class="data-row"
      >
        <!-- 은행명 -->
        <td>{{ saving.kor_co_nm }}</td>
        <!-- 상품명 -->
        <td>{{ saving.fin_prdt_nm }}</td>
        <!-- 각 기간별 금리 -->
        <td
          v-for="period in periods"
          :key="'data-' + period"
          class="interest-rate"
        >
          <span
            v-if="saving.options.find(option => option.save_trm === period)?.intr_rate"
          >
            {{
              saving.options.find(option => option.save_trm === period).intr_rate
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
  savings: Array, // 적금 데이터 배열
  periods: Array, // 기간 배열
});

const router = useRouter();

// 상세 페이지로 이동
const goToDetail = (id) => {
  router.push({ name: 'SavingDetailView', params: { product_id: id } });
};
</script>

<style scoped>
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
