<template>
  <div class="data-row">
    <div @click="goToDetail" class="saving-item">
      <p>{{ saving.id}}</p>
    </div>
    <!-- 은행명 -->
    <span class="data-item">{{ saving.kor_co_nm }}</span>
    <!-- 상품명 -->
    <span class="data-item">{{ saving.fin_prdt_nm }}</span>
    <!-- 금리 -->
    <span
      v-for="period in [6, 12, 24, 36]"
      :key="'rate-' + period"
      class="data-item"
      :class="{ highlight: period === highlightPeriod }"
    >
      <span v-if="saving.options.find(option => option.save_trm === period)?.intr_rate">
        {{ saving.options.find(option => option.save_trm === period).intr_rate }}%
      </span>
      <span v-else>-</span>
    </span>
  </div>
</template>

<script setup>
const props = defineProps({
  saving: Object, // 단일 예금 데이터
  highlightPeriod: {
    type: Number, // 강조할 기간
    default: 0,
  },
});

import { useRouter } from 'vue-router';
const router = useRouter()
const goToDetail = () => {
  router.push(`/finance/saving/${props.saving.id}`)
}


</script>

<style scoped>
.data-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  background-color: white;
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
</style>
