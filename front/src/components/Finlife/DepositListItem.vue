<template>
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

const props = defineProps({
  deposit: Object, // 단일 예금 데이터
  highlightPeriod: {
    type: Number, // 강조할 기간
    default: 0,
  },
});

const router = useRouter();

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
};
</script>

<style scoped>
.data-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  background-color: white;
  cursor: pointer;
}

.data-item {
  flex: 1;
  text-align: center;
  font-size: 1rem;
  color: #34495e;
}

.data-item span {
  font-weight: bold;
  color: #27ae60;
}

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
</style>
