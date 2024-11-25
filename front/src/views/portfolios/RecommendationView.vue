<template>
  <v-container class="recommendation-container">
    <v-card class="recommendation-card" elevation="2">
      <v-card-title>
        <h2>추천 상품</h2>
      </v-card-title>
      <v-card-text>
        <v-alert v-if="errorMessage" type="error" dense class="mb-3">
          {{ errorMessage }}
        </v-alert>
        <v-alert v-if="!recommendations.length && !errorMessage" type="info" dense>
          추천 상품이 없습니다. 포트폴리오 데이터를 확인해주세요.
        </v-alert>

        <v-list dense v-if="recommendations.length">
          <v-list-item
            v-for="(item, index) in recommendations"
            :key="index"
            class="recommendation-item"
          >
            <v-list-item-content>
              <v-list-item-title>
                {{ item.fin_prdt_nm }} ({{ item.kor_co_nm }})
              </v-list-item-title>
              <v-list-item-subtitle>
                최고 금리: {{ item.max_rate }}%<br />
                조건: {{ item.conditions }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>

      <!-- 뒤로가기 버튼 -->
      <v-card-actions>
        <v-btn color="secondary" @click="goBack">뒤로 가기</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const recommendations = ref([]);
const errorMessage = ref("");
const route = useRoute();
const router = useRouter();

// 포트폴리오 ID 가져오기
const portfolioId = route.params.portfolioId;

// API에서 추천 데이터 가져오기
const fetchRecommendations = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/portfolios/${portfolioId}/recommend/`
    );
    recommendations.value = response.data.recommended_deposits || [];
  } catch (error) {
    errorMessage.value =
      error.response?.data?.error || "추천 데이터를 불러오지 못했습니다.";
  }
};

// 페이지 마운트 시 데이터 가져오기
onMounted(() => {
  fetchRecommendations();
});

// 뒤로 가기
const goBack = () => {
  router.push({ name: "ProfileView" });
};
</script>

<style scoped>
.recommendation-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  max-width: 800px;
}

.recommendation-card {
  padding: 20px;
  width: 100%;
}

.recommendation-item {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}

.v-list-item-title {
  font-weight: bold;
  color: #333;
}

.v-list-item-subtitle {
  color: #666;
}
</style>
