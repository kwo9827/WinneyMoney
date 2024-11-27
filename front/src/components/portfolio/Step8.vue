<template>
  <v-container class="completion-container">
    <v-card elevation="2" class="completion-card">
      <v-card-title class="title">
        <h2>🎉 포트폴리오 생성 완료!</h2>
      </v-card-title>
      <v-card-text>
        <p>포트폴리오 이름: <strong>{{ portfolio.name }}</strong></p>
        <p>총 투자 금액: <strong>{{ portfolio.total_investment }} ₩</strong></p>
        <p>경제 전망: <strong>{{ getEconomyLabel(portfolio.predicted_economy) }}</strong></p>
        <p>투자 성향: <strong>{{ getRiskLabel(portfolio.risk_preference) }}</strong></p>
        <v-divider class="my-3"></v-divider>
        <p>포트폴리오가 성공적으로 생성되었습니다. 아래 옵션에서 다음 작업을 선택하세요:</p>
        
        <v-btn color="primary" @click="goToRecommendations(portfolioId)" class="mt-3" block>
          추천 상품 보기
        </v-btn>
        <v-btn color="secondary" @click="goToProfile" class="mt-3" block>
          내 포트폴리오 보기
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { usePortfolioStore } from "@/stores/portfolio";
import { useRouter } from "vue-router";

// 포트폴리오 데이터 가져오기
const portfolioStore = usePortfolioStore();
const portfolio = portfolioStore.portfolio;
const portfolioId = portfolioStore.portfolioId
const router = useRouter();

// 금액 포맷 함수
const formattedInvestment = new Intl.NumberFormat("ko-KR").format(
  portfolio.totalInvestment
);

// 라벨 매핑 함수
const getEconomyLabel = (value) => {
  const labels = {
    growth: "성장",
    recession: "하락",
    stability: "유지",
  };
  return labels[value] || "알 수 없음";
};

const getRiskLabel = (value) => {
  const labels = {
    low: "수비적",
    medium: "보통",
    high: "공격형",
  };
  return labels[value] || "알 수 없음";
};

// 추천 상품 페이지 이동
const goToRecommendations = (id) => {
  router.push({ name: "RecommendationView" , params: { portfolioId: id }});
};

// 내 포트폴리오 페이지 이동
const goToProfile = () => {
  router.push({ name: "ProfileView" });
};
</script>

<style scoped>
.completion-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.completion-card {
  padding: 20px;
  max-width: 500px;
  width: 100%;
  text-align: center;
  background-color: #ffffff;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.my-3 {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>
