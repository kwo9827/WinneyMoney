<template>
  <v-container class="container">
    <!-- 진행 바 -->
    <div class="progress-tick-container mb-4">
      <div class="progress-tick-bar">
        <div class="progress-tick-fill" :style="progressBarStyle"></div>
        <div
          v-for="(tick, index) in totalSteps"
          :key="index"
          class="progress-tick"
          :class="{ active: currentStep >= index }"
        ></div>
      </div>
      <div class="progress-tick-label">
        {{ currentStep + 1 }} / {{ totalSteps }} 단계
      </div>
    </div>

    <!-- 단계별 카드 -->
    <v-card
      class="card"
      :class="{ 'slide-in': !isSlidingOut, 'slide-out': isSlidingOut }"
      elevation="2"
    >
      <v-card-title>
        <h1 v-if="currentStep < totalSteps - 1">포트폴리오 생성</h1>
        <h1 v-else>포트폴리오 생성 완료!</h1>
      </v-card-title>

      <v-card-text>
        <v-alert v-if="errorMessage" type="error" dense class="mb-3">
          {{ errorMessage }}
        </v-alert>
        <Step1 v-if="currentStep === 0" @next="validateAndNext" />
        <Step2 v-if="currentStep === 1" @next="validateAndNext" @prev="changeStep('prev')" />
        <Step3 v-if="currentStep === 2" @next="validateAndNext" @prev="changeStep('prev')" />
        <Step4 v-if="currentStep === 3" @next="validateAndNext" @prev="changeStep('prev')" />
        <Step5 v-if="currentStep === 4" @next="validateAndNext" />
        <Step6 v-if="currentStep === 5" @submit="submitPortfolio" @prev="changeStep('prev')"/>
        <Step7 v-if="currentStep === 6" />
      </v-card-text>
    </v-card>

    <!-- 로딩 오버레이 -->
    <v-overlay :value="isLoading" absolute>
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <span>잠시만 기다려주세요...</span>
    </v-overlay>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";
import Step1 from "@/components/portfolio/Step1.vue";
import Step2 from "@/components/portfolio/Step2.vue";
import Step3 from "@/components/portfolio/Step3.vue";
import Step4 from "@/components/portfolio/Step4.vue";
import Step5 from "@/components/portfolio/Step5.vue";
import Step6 from "@/components/portfolio/Step6.vue";
import Step7 from "@/components/portfolio/Step7.vue";

const currentStep = ref(0);
const totalSteps = 7; // 총 단계 수
const portfolioStore = usePortfolioStore();
const isLoading = ref(false);
const errorMessage = ref("");
const isSlidingOut = ref(false);

// 진행 바 스타일 계산
const progressBarStyle = computed(() => ({
  width: `${((currentStep.value + 1) / totalSteps) * 100}%`,
}));

// 단계 변경 로직
const changeStep = (direction) => {
  if (isSlidingOut.value) return;

  isSlidingOut.value = true;

  setTimeout(() => {
    isSlidingOut.value = false;
    if (direction === "next" && currentStep.value < totalSteps - 1) {
      currentStep.value++;
    } else if (direction === "prev" && currentStep.value > 0) {
      currentStep.value--;
    }
  }, 500);
};

// 다음 단계로 이동
const validateAndNext = () => {
  changeStep("next");
};

// 포트폴리오 제출
const submitPortfolio = async () => {
  try {
    isLoading.value = true;
    alert("포트폴리오 생성 완료!");
    changeStep("next");
  } catch (error) {
    errorMessage.value = "포트폴리오 생성 중 오류가 발생했습니다. 다시 시도해주세요.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  max-width: 600px;
}

/* 눈금 스타일 */
.progress-tick-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.progress-tick-bar {
  position: relative;
  width: 100%;
  height: px;
  background-color: #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.progress-tick-fill {
  position: absolute;
  height: 100%;
  background-color: #007bff;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-tick {
  position: relative;
  width: 12px;
  height: 12px;
  background-color: #ddd;
  border: 2px solid white;
  border-radius: 50%;
  z-index: 1;
  margin-left: auto;
  margin-right: auto;
}

.progress-tick.active {
  background-color: #007bff;
}

.progress-tick:not(:first-child) {
  margin-left: calc(-6px);
}

.progress-tick-label {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

/* 카드 스타일 */
.card {
  padding: 20px;
  width: 100%;
  max-width: 1000px;
  opacity: 0;
  transform: translateX(100%);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.card.slide-in {
  opacity: 1;
  transform: translateX(0);
}

.card.slide-out {
  opacity: 0;
  transform: translateX(-100%);
}
</style>

