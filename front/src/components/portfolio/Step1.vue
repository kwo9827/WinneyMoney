<template>
  <v-container>
    <v-card class="pa-4" width="100%">
      <v-card-title>
        <h2>포트폴리오 이름 설정</h2>
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="portfolio.name"
          label="포트폴리오 이름"
          outlined
          dense
          placeholder="예: '내 첫 투자'"
          @input="validateInput"
        />
        <v-alert v-if="error" type="error" class="mt-2">
          {{ error }}
        </v-alert>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" :disabled="!portfolio.name" @click="nextStep">
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

const portfolio = usePortfolioStore().portfolio;
const error = ref("");

// 이벤트 정의
const emit = defineEmits(["next"]);

// 입력 실시간 검증
const validateInput = () => {
  if (portfolio.name.length > 20) {
    error.value = "포트폴리오 이름은 20자 이하로 입력해주세요.";
  } else {
    error.value = "";
  }
};

// 다음 단계로 이동
const nextStep = () => {
  if (!portfolio.name) {
    error.value = "포트폴리오 이름을 입력해주세요.";
  } else if (portfolio.name.length > 20) {
    error.value = "포트폴리오 이름은 20자 이하로 입력해주세요.";
  } else {
    error.value = "";
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
  width: 100%;
}

.v-alert {
  font-size: 0.9rem;
}
</style>
