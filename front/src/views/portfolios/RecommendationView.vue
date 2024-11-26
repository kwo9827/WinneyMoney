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
        <!-- 차트 -->
        <div class="chart-container">
          <PieChart :chart-data="chartData" :options="chartOptions" />
        </div>
        <!-- 변동성 설명 -->
        <v-alert type="info" dense>
          고객님의 포트폴리오 변동성은 <strong>{{ recommendations.portfolio.volatility || 'N/A' }}</strong>입니다.
        </v-alert>
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
              <p class="recommendation-description">추천 이유:</p>
              <ul class="recommendation-reasons">
                <li v-for="(reason, idx) in item.reason.split('\n')" :key="idx">
                  {{ reason }}
                </li>
              </ul>
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
const chartData = ref({
  labels: ["Stocks", "Cryptocurrencies", "Others"],
  datasets: [
    {
      data: [0, 0, 0], // 초기값 설정
      backgroundColor: ["#42A5F5", "#66BB6A", "#FFA726"],
      hoverBackgroundColor: ["#64B5F6", "#81C784", "#FFB74D"],
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
          const total = chartData.value.datasets[0].data.reduce((acc, cur) => acc + cur, 0);
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

    // 차트 데이터 업데이트
    const stockInvestment = recommendations.value?.portfolio?.stocks || 0;
    const cryptoInvestment = recommendations.value?.portfolio?.cryptocurrencies || 0;
    const otherInvestment = recommendations.value?.portfolio?.others || 0;

    chartData.value.datasets[0].data = [stockInvestment, cryptoInvestment, otherInvestment];
  } catch (error) {
    errorMessage.value = error.message || "추천 데이터를 불러오지 못했습니다.";
  }
};

// 페이지 마운트 시 데이터 가져오기
onMounted(() => {
  console.log("포트폴리오 ID:", portfolioId);
  fetchRecommendations(portfolioId);
});

// 뒤로 가기
const goBack = () => {
  router.push({ name: "ProfileView" });
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
  height: 500px; /* 차트 높이를 늘려 더 보기 쉽게 조정 */
  margin-bottom: 20px;
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

.recommendation-image {
  border-radius: 10px 10px 0 0;
}

.recommendation-title {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
}

.recommendation-description {
  font-size: 1rem;
  color: #555;
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
</style>
