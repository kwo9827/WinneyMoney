<template>
  <div class="container">
    <h1>포트폴리오 생성</h1>
    <!-- 각 단계별 컴포넌트 렌더링 -->
    <Step1 v-if="currentStep === 0" @next="nextStep" />
    <Step2 v-if="currentStep === 1" @next="nextStep" />
    <Step3 v-if="currentStep === 2" @next="nextStep" />
    <Step4 v-if="currentStep === 3" @next="nextStep" />
    <Step5 v-if="currentStep === 4" @submit="submitPortfolio" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";
import Step1 from "@/components/portfolio/Step1.vue";
import Step2 from "@/components/portfolio/Step2.vue";
import Step3 from "@/components/portfolio/Step3.vue";
import Step4 from "@/components/portfolio/Step4.vue";
import Step5 from "@/components/portfolio/Step5.vue";

const currentStep = ref(0);
const portfolioStore = usePortfolioStore();

// 다음 단계로 이동
const nextStep = () => {
  currentStep.value++;
};

// 포트폴리오 제출
const submitPortfolio = async () => {
  try {
    await portfolioStore.createPortfolio();
    alert("포트폴리오 생성 완료!");
  } catch (error) {
    console.error("에러 발생:", error);
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}
</style>
