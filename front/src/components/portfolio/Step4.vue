<template>
  <v-container>
    <v-card class="pa-4" width="100%">
      <v-card-title>
        <h2>경제 전망 선택</h2>
      </v-card-title>
      <v-card-text>
        <v-select
          v-model="portfolio.predicted_economy"
          :items="economyOptions"
          item-title="text"
          item-value="value"
          label="경제 전망"
          outlined
          dense
          clearable
          persistent-hint
          hint="예: 성장, 하락, 안정 중 선택"
          @change="clearError"
        />
        <p class="helper-text">
          선택한 경제 전망에 따라 추천 상품이 달라집니다.
        </p>
        <v-alert v-if="error" type="error" class="mt-2">
          {{ error }}
        </v-alert>
      </v-card-text>

      <v-card-actions class="action-buttons">
        <!-- 이전 버튼 -->
        <v-col cols="6">
          <v-btn color="secondary" block @click="emit('prev')">
            이전
          </v-btn>
        </v-col>
        <!-- 다음 버튼 -->
        <v-col cols="6">
          <v-btn
            color="primary"
            block
            :disabled="!portfolio.predicted_economy"
            @click="nextStep"
          >
            다음
          </v-btn>
        </v-col>
      </v-card-actions>

    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";
import { defineEmits } from "vue";

const portfolio = usePortfolioStore().portfolio;
const error = ref("");

// 경제 전망 옵션
const economyOptions = ref([
  { text: "성장 (Growth)", value: "growth" },
  { text: "하락 (Recession)", value: "recession" },
  { text: "안정 (Stability)", value: "stability" },
]);

// 이벤트 정의
const emit = defineEmits(["next", "prev"]);

// 다음 단계로 이동
const nextStep = () => {
  if (!portfolio.predicted_economy) {
    error.value = "경제 전망을 선택해주세요.";
  } else {
    error.value = "";
    emit("next");
  }
};

const prevStep = () => {
  emit("prev");
};

// 오류 초기화
const clearError = () => {
  if (portfolio.predicted_economy) {
    error.value = "";
  }
};
</script>

<style scoped>
.v-container {
  max-width: 400px;
  margin: 0 auto;
}

.v-btn {
  width: 100%;
}

.v-alert {
  font-size: 0.9rem;
}

.helper-text {
  font-size: 0.8rem;
  color: #666;
  margin-top: 4px;
}
</style>
