<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>
        <h2>현재 가용 가능한 자금 입력</h2>
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="portfolio.current_cash"
          label="가용 자금 (₩)"
          outlined
          dense
          placeholder="예: 1000000 (숫자만 입력)"
          clearable
          type="number"
          :error-messages="error"
          @input="validateInput"
        />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" :disabled="!isInputValid" @click="nextStep">
          다음
        </v-btn>
        <v-btn color="secondary" outlined @click="emit('prev')">
          이전
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";
import { defineEmits } from "vue";

const portfolio = usePortfolioStore().portfolio;
portfolio.current_cash = portfolio.current_cash || 0; // 초기 값 설정

const error = ref("");
const emit = defineEmits(["next", "prev"]);

// 입력 유효성 검사
const validateInput = () => {
  if (portfolio.current_cash < 0) {
    error.value = "가용 자금은 0 이상이어야 합니다.";
  } else {
    error.value = "";
  }
};

// 입력 유효성 상태
const isInputValid = computed(() => {
  return portfolio.current_cash >= 0 && error.value === "";
});

// 다음 단계로 이동
const nextStep = () => {
  if (!isInputValid.value) {
    error.value = "가용 자금을 올바르게 입력해주세요.";
  } else {
    emit("next");
  }
};
</script>

<style scoped>
.v-container {
  max-width: 400px;
  margin: 0 auto;
}

.v-btn {
  width: auto;
  min-width: 120px;
}

.v-alert {
  font-size: 0.9rem;
}
</style>
