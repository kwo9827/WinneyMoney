<template>
  <v-container class="step-container">
    <v-card class="card" elevation="2">
      <v-card-title>
        <h2>위험 성향 선택</h2>
      </v-card-title>

      <v-card-text>
        <div class="option-container">
          <div
            v-for="option in riskOptions"
            :key="option.value"
            class="risk-option"
            :class="{ 'selected': portfolio.riskPreference === option.value }"
            @click="selectOption(option.value)"
          >
            <p class="option-title">{{ option.label }}</p>
            <p class="option-description">{{ option.description }}</p>
          </div>
        </div>
        <v-alert v-if="error" type="error" class="mt-2">
          {{ error }}
        </v-alert>
      </v-card-text>

      <v-card-actions>
        <v-btn
          :disabled="!portfolio.riskPreference"
          @click="nextStep"
          color="primary"
        >
          다음
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";
import { defineEmits } from "vue";

const emit = defineEmits(["next"]);
const portfolio = usePortfolioStore().portfolio;
const error = ref("");

// 위험 성향 옵션
const riskOptions = [
  {
    label: "수비적",
    value: "low",
    description: "낮은 위험, 안정적 수익",
  },
  {
    label: "보통",
    value: "medium",
    description: "중간 위험, 균형 잡힌 수익",
  },
  {
    label: "공격형",
    value: "high",
    description: "높은 위험, 높은 수익 가능성",
  },
];

// 옵션 선택
const selectOption = (value) => {
  portfolio.riskPreference = value;
  error.value = "";
};

// 다음 단계로 이동
const nextStep = () => {
  if (!portfolio.riskPreference) {
    error.value = "위험 성향을 선택해주세요.";
  } else {
    error.value = "";
    emit("next");
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
  margin-bottom: 10px;
  color: #333;
}

.option-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.risk-option {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  background-color: white;
}

.risk-option:hover {
  transform: translateY(-3px);
  background-color: #f5f5f5;
}

.risk-option.selected {
  background-color: #1976d2;
  color: rgb(255, 249, 249);
  font-weight: bold;
  border: 1px solid #1976d2;
}

.option-title {
  font-size: 1rem;
  font-weight: bold;
  margin: 0;
}

.option-description {
  font-size: 0.9rem;
  margin: 0;
}

.v-btn {
  width: 100%;
}

.v-alert {
  font-size: 0.9rem;
  margin-top: 10px;
}
</style>
