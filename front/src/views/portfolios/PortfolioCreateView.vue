<template>
  <v-container class="container">
    <!-- 실린더 프로그레스 바 -->
    <div class="cylinder-progress-container mb-4">
      <div class="cylinder">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle class="cylinder-bg" cx="50" cy="50" r="45"></circle>
          <circle
            class="cylinder-fill"
            cx="50"
            cy="50"
            r="45"
            :style="fillStyle"
          ></circle>
        </svg>
        <div class="cylinder-label">
          {{ currentStep + 1 }} / 7 단계
        </div>
      </div>
    </div>

    <!-- 단계별 카드 -->
    <v-card
      class="card"
      :class="{ 'slide-in': !isSlidingOut, 'slide-out': isSlidingOut }"
      elevation="2"
    >
      <v-card-title>
        <h1 v-if="currentStep < 6">포트폴리오 생성</h1>
        <h1 v-else>포트폴리오 생성 완료!</h1>
      </v-card-title>

      <v-card-text>
        <v-alert v-if="errorMessage" type="error" dense class="mb-3">
          {{ errorMessage }}
        </v-alert>
        <Step1 v-if="currentStep === 0" @next="validateAndNext" />
        <Step2 v-if="currentStep === 1" @next="validateAndNext" />
        <Step3 v-if="currentStep === 2" @next="validateAndNext" />
        <Step4 v-if="currentStep === 3" @next="validateAndNext" />
        <Step5 v-if="currentStep === 4" @next="validateAndNext" />
        <Step6 v-if="currentStep === 5" @submit="submitPortfolio" />
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
import Step5 from "@/components/portfolio/Step5.vue"; // 주식 추가
import Step6 from "@/components/portfolio/Step6.vue"; // 암호화폐 추가
import Step7 from "@/components/portfolio/Step7.vue"; // 포트폴리오 생성 완료

const currentStep = ref(0);
const portfolioStore = usePortfolioStore();
const isLoading = ref(false);
const errorMessage = ref("");
const isSlidingOut = ref(false); // 슬라이드 아웃 상태

// 진행 상태 계산
const progressPercentage = computed(() => ((currentStep.value + 1) / 7) * 100);

const fillStyle = computed(() => {
  const progress = 283 - (283 * progressPercentage.value) / 100; // Stroke offset 계산
  return {
    strokeDashoffset: progress,
  };
});

// 각 단계 데이터의 유효성 검사
const validateStep = () => {
  switch (currentStep.value) {
    case 0:
      return portfolioStore.portfolio.name !== ""; // Step1: 이름 입력 확인
    case 1:
      return portfolioStore.portfolio.predictedEconomy !== null; // Step2: 경제 상황 입력 확인
    case 2:
      return portfolioStore.portfolio.riskPreference !== null; // Step3: 리스크 선호도 확인
    case 3:
      return portfolioStore.portfolio.totalInvestment > 0; // Step4: 투자 금액 확인
    default:
      return true; // 주식, 암호화폐 단계는 개별적으로 처리
  }
};

// 단계 변경 (슬라이딩 효과 포함)
const changeStep = (direction) => {
  if (isLoading.value) return; // 로딩 중에는 이동 방지

  isSlidingOut.value = true; // 슬라이드 아웃 시작
  setTimeout(() => {
    isSlidingOut.value = false; // 슬라이드 인 준비
    if (direction === "next" && validateStep()) {
      errorMessage.value = "";
      currentStep.value++;
    } else if (direction === "prev" && currentStep.value > 0) {
      currentStep.value--;
    } else {
      errorMessage.value = "모든 정보를 올바르게 입력해주세요!";
    }
  }, 500); // 애니메이션 시간과 일치
};

// 다음 단계로 이동
const validateAndNext = () => {
  changeStep("next");
};

// 포트폴리오 제출
const submitPortfolio = async () => {
  try {
    isLoading.value = true;
    await portfolioStore.createPortfolio();
    alert("포트폴리오 생성 완료!");
    changeStep("next");
    console.log("현재 단계:", currentStep.value);
    console.log("포트폴리오 데이터:", portfolioStore.portfolio);
  } catch (error) {
    console.error("에러 발생:", error.message || error);
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

/* 실린더 프로그레스 바 스타일 */
.cylinder-progress-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.cylinder {
  position: relative;
  width: 100px;
  height: 100px;
}

.cylinder-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.cylinder svg {
  transform: rotate(-90deg); /* 위에서 아래로 채워지도록 */
  width: 100%;
  height: 100%;
}

.cylinder-bg {
  fill: none;
  stroke: #ddd;
  stroke-width: 10;
}

.cylinder-fill {
  fill: none;
  stroke: #007bff;
  stroke-width: 10;
  stroke-linecap: round;
  stroke-dasharray: 283; /* 전체 원 둘레 */
  stroke-dashoffset: 283; /* 기본값 (빈 상태) */
  transition: stroke-dashoffset 0.6s ease;
}

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

h1 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.mb-4 {
  margin-bottom: 16px;
}

.v-alert {
  font-size: 0.9rem;
}

.v-overlay {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
}
</style>
