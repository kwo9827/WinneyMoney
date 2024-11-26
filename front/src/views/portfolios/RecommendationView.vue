<template>
  <v-container class="recommendation-container">
    <!-- 로드 중 상태 -->
    <div v-if="!recommendations?.portfolio">
      데이터를 로드 중입니다...
    </div>

    <!-- 포트폴리오 정보 -->
    <v-card v-if="recommendations?.portfolio" class="portfolio-summary-card" elevation="2">
      <v-card-title>
        <h2>{{ recommendations.portfolio.name }} 포트폴리오</h2>
      </v-card-title>
      <v-card-text>
        <!-- 총 투자 금액과 변동성 -->
        <p><strong>총 투자 금액:</strong> {{ formatCurrency(recommendations.portfolio.total_investment) }}</p>
        <p><strong>현재 포트폴리오 변동성:</strong> {{ recommendations.portfolio.total_volatility?.toFixed(2) || 'N/A' }}</p>

        <!-- 차트 병렬 배치 -->
        <v-row>
          <v-col cols="12" md="6">
            <div class="chart-container">
              <h3>현재 비율</h3>
              <PieChart :chart-data="currentChartData" :options="chartOptions" />
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="chart-container">
              <h3>추천 비율</h3>
              <PieChart :chart-data="recommendedChartData" :options="chartOptions" />
            </div>
          </v-col>
        </v-row>

        <!-- 변동성 변화 -->
        <div class="volatility-section">
          <p><strong>추천 후 예상 변동성:</strong> {{ recommendations.recommendations[0].recommended_volatility.toFixed(2) || 'N/A' }}</p>
          <p><em>추천 상품에 따른 변동성 변경을 확인하세요.</em></p>
          <!-- {{ recommendations.recommendations[3] }} -->
          <!-- {{ recommendations.investment_allocation }}
           {{ recommendations.saving_allocation }} 
          {{ recommendations.recommendations[0].recommended_volatility }} -->
        </div>
      </v-card-text>
    </v-card>

    <!-- 추천 상품 -->
    <v-card class="recommendation-card" elevation="2">
      <v-card-title>
        <h3>추천 상품</h3>
      </v-card-title>
      <v-card-text>
        <v-alert v-if="errorMessage" type="error" dense class="mb-3">
          {{ errorMessage }}
        </v-alert>

        <v-alert v-if="!recommendations.recommendations?.length && !errorMessage" type="info" dense>
          추천 상품이 없습니다. 포트폴리오 데이터를 확인해주세요.
        </v-alert>

        <div class="recommendations-grid" v-if="recommendations?.recommendations?.length">
          <v-card
            v-for="(item, index) in recommendations.recommendations"
            :key="index"
            class="recommendation-item"
            outlined
          >
            <!-- item.bank_name 확인을 위한 콘솔 출력 -->
            <div>{{ console.log(item.bank_name) }}</div> <!-- 여기서 콘솔로 item.bank_name 출력 -->
            <div>{{ console.log(item) }}</div>
            <!-- 은행 이미지 동적 바인딩 -->
            <!-- <v-img
              :src="getBankImage(item.bank_name)"  
              alt="Bank Logo"
              height="150"
              class="recommendation-image"
            /> -->
            
            <v-card-title class="recommendation-title">
              {{ item.product_name }}
              <span class="product-type">({{ item.product_type }})</span>
            </v-card-title>
            
            <v-card-text>
              <p class="recommendation-description"><strong>추천 이유:</strong></p>
              <ul class="recommendation-reasons">
                <li v-for="(reason, idx) in item.reason.split(' | ')" :key="idx">
                  {{ reason }}
                </li>
              </ul>
              <p class="recommended-amount">
                <strong>추천 금액:</strong> {{ formatCurrency(item.recommended_amount) }}
              </p>
            </v-card-text>

            <v-card-actions>
              <v-btn
                v-if="item.product_type === 'Deposit'" 
                :to="{ name: 'DepositPortDetailView', params: { product_id: item.product_id, portfolio_id: route.params.portfolioId } }"
                color="primary"
                block
                outlined
              >
                자세히 보기
              </v-btn>
              <v-btn
                v-else-if="item.product_type === 'Saving'" 
                :to="{ name: 'SavingPortDetailView', params: { product_id: item.product_id, portfolio_id: route.params.portfolioId } }"
                color="primary"
                block
                outlined
              >
                자세히 보기
              </v-btn>
            </v-card-actions>
          </v-card>

        </div>
      </v-card-text>

      <!-- 뒤로가기 버튼 -->
      <v-card-actions>
        <v-btn color="secondary" @click="goBack" block>뒤로 가기</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { usePortfolioStore } from "@/stores/portfolio";
import { PieChart } from "vue-chart-3";
import { Chart, PieController, ArcElement, Tooltip, Legend } from "chart.js";

// Chart.js 컴포넌트 등록
Chart.register(PieController, ArcElement, Tooltip, Legend);

const recommendations = ref({});
const errorMessage = ref("");
const route = useRoute();
const router = useRouter();
const portfolioStore = usePortfolioStore();

const portfolioId = route.params.portfolioId;

// 차트 데이터 및 옵션
const currentChartData = ref({
  labels: ["주식", "암호화폐", "예금", "적금", "현금"],
  datasets: [
    {
      data: [0, 0, 0, 0, 0],
      backgroundColor: ["#FF9AA2", "#FFB7B2", "#FFDAC1", "#E2F0CB", "#B5EAD7"],
      hoverBackgroundColor: ["#FF9AA2", "#FFB7B2", "#FFDAC1", "#E2F0CB", "#B5EAD7"],
    },
  ],
});

const recommendedChartData = ref({
  labels: ["주식", "암호화폐", "예금", "적금", "현금"],
  datasets: [
    {
      data: [0, 0, 0, 0, 0],
      backgroundColor: ["#C7CEEA", "#B5EAD7", "#E2F0CB", "#FFDAC1", "#FFB7B2"],
      hoverBackgroundColor: ["#C7CEEA", "#B5EAD7", "#E2F0CB", "#FFDAC1", "#FFB7B2"],
    },
  ],
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: "bottom",
    },
    tooltip: {
      callbacks: {
        label: function (tooltipItem) {
          const value = tooltipItem.raw;
          const total = tooltipItem.dataset.data.reduce((acc, cur) => acc + cur, 0);
          const percentage = ((value / total) * 100).toFixed(2);
          return `${tooltipItem.label}: ${percentage}%`;
        },
      },
    },
  },
});

// 추천 데이터 가져오기
const fetchRecommendations = async (portfolioId) => {
  if (!portfolioId) {
    errorMessage.value = "포트폴리오가 생성되지 않았습니다.";
    return;
  }

  try {
    const data = await portfolioStore.fetchRecommendations(portfolioId);
    recommendations.value = data;

    // 현재 비율 차트 데이터 업데이트
    const currentAllocation = recommendations.value?.portfolio?.allocation || {};
    currentChartData.value.datasets[0].data = [
      currentAllocation.stock || 0,
      currentAllocation.crypto || 0,
      currentAllocation.deposit || 0,
      currentAllocation.saving || 0,
      currentAllocation.cash || 0,
    ];

    // 추천 비율 차트 데이터 업데이트
    const recommendedAllocation = recommendations.value?.investment_allocation || {};
    const savingAllocation = recommendations.value?.saving_allocation || {};
    recommendedChartData.value.datasets[0].data = [
      recommendedAllocation.stock || 0,
      recommendedAllocation.crypto || 0,
      savingAllocation.deposit || 0,
      savingAllocation.saving || 0,
      0, // 현금
    ];
  } catch (error) {
    errorMessage.value = error.message || "추천 데이터를 불러오지 못했습니다.";
  }
};

// 페이지 마운트 시 데이터 가져오기
onMounted(() => {
  fetchRecommendations(portfolioId);
});

// 뒤로 가기
const goBack = () => {
  router.push({ name: "ProfileView" });
};

// 금액 포맷 함수
const formatCurrency = (value) => {
  return new Intl.NumberFormat("ko-KR", {
    style: "currency",
    currency: "KRW",
  }).format(value);
};
// 은행 이미지 
const getBankImage = (bankName) => {
  const bankImages = import.meta.glob('@/assets/bank-images/*.png');

  // bankName에 해당하는 이미지 경로 찾기
  const imagePath = `@/assets/bank-images/${bankName}.png`;
  const image = bankImages[imagePath];

  // 이미지가 없으면 기본 이미지를 반환
  return image || bankImages['@/assets/bank-images/default.jpg'];
};

</script>

<style scoped>
.recommendation-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  max-width: 1000px;
}

.portfolio-summary-card {
  width: 100%;
  padding: 20px;
}

.chart-container {
  width: 100%;
  height: 400px;
  margin-bottom: 20px;
}

.volatility-section {
  margin-top: 10px;
  font-size: 1rem;
  color: #555;
}

.recommendation-card {
  width: 100%;
  padding: 20px;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.recommendation-item {
  padding: 16px;
  border-radius: 10px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.recommendation-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.recommendation-title {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
}

.recommendation-reasons {
  list-style: disc;
  padding-left: 20px;
}

.product-type {
  font-size: 0.9rem;
  color: #888;
  margin-left: 5px;
}

.recommended-amount {
  font-size: 1rem;
  font-weight: bold;
  margin-top: 10px;
}
</style>
