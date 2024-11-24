<template>
  <v-container class="step-container">
    <v-card class="card" elevation="2">
      <v-card-title>
        <h2>초기 투자 금액 입력</h2>
      </v-card-title>

      <v-card-text>
        <v-text-field
          label="초기 투자 금액"
          v-model="formattedInvestment"
          type="text"
          placeholder="금액을 입력하세요"
          outlined
          color="primary"
          @input="clearError"
          @blur="formatInvestment"
        >
          <template #append>
            <span class="currency-symbol">원(₩)</span>
          </template>
        </v-text-field>
        <v-alert v-if="error" type="error" dense class="mt-2">
          {{ error }}
        </v-alert>
      </v-card-text>

      <v-card-actions>
        <v-btn
          :disabled="!portfolio.totalInvestment || portfolio.totalInvestment <= 0 || isLoading"
          @click="submitPortfolio"
          :color="isLoading ? 'grey' : 'primary'"
        >
          {{ isLoading ? '생성 중...' : '포트폴리오 생성' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, watch } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";
import { defineEmits } from "vue";

const emit = defineEmits(["next"]);
const portfolioStore = usePortfolioStore();
const portfolio = portfolioStore.portfolio;
const error = ref("");
const isLoading = ref(false);

// 사용자가 입력한 포맷팅된 금액
const formattedInvestment = ref("");

// 숫자 입력 초기화
watch(
  () => portfolio.totalInvestment,
  (newValue) => {
    formattedInvestment.value = newValue
      ? newValue.toLocaleString()
      : "";
  },
  { immediate: true }
);

// 에러 초기화
const clearError = () => {
  error.value = "";
};

// 금액 포맷팅 적용
const formatInvestment = () => {
  const numericValue = Number(
    formattedInvestment.value.replace(/[^\d]/g, "")
  );
  if (numericValue > 0) {
    portfolio.totalInvestment = numericValue;
    formattedInvestment.value = numericValue.toLocaleString();
  } else {
    error.value = "올바른 투자 금액을 입력해주세요.";
    portfolio.totalInvestment = 0;
  }
};

// 포트폴리오 생성 및 다음 단계로 이동
const submitPortfolio = async () => {
  try {
    isLoading.value = true;
    const response = await portfolioStore.createPortfolio();
    console.log("포트폴리오 생성 성공:", response);
    alert("포트폴리오가 성공적으로 생성되었습니다!");
    emit("next");
  } catch (error) {
    console.error("포트폴리오 생성 실패:", error.message || error);
    alert("포트폴리오 생성에 실패했습니다. 다시 시도해주세요.");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.step-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  max-width: 500px;
}

.card {
  padding: 20px;
  width: 100%;
}

h2 {
  font-size: 1.4rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.currency-symbol {
  font-weight: bold;
  color: #333;
}

.v-btn {
  width: 100%;
}

.v-alert {
  font-size: 0.9rem;
  margin-top: 10px;
  color: red;
}
</style>
