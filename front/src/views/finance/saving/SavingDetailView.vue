<template>
  <div class="container">
    <!-- 상품 정보 카드 -->
    <div class="detail-card">
      <h1 class="title">{{ saving.kor_co_nm }} - {{ saving.fin_prdt_nm }}</h1>
      <p class="subtitle">가입 방법: {{ saving.join_way }}</p>
      <p class="subtitle">만기 후 이자율: {{ saving.mtrt_int }}</p>
      <p class="subtitle">우대 조건: {{ saving.spcl_cnd }}</p>
      <p class="subtitle">
        가입 제한:
        <span v-if="saving.join_deny === 1">제한 없음</span>
        <span v-else-if="saving.join_deny === 2">서민 전용</span>
        <span v-else-if="saving.join_deny === 3">일부 제한</span>
        <span v-else>정보 없음</span>
      </p>
      <p class="subtitle">
        최고 한도: {{ saving.max_limit === -1 ? '제한 없음' : saving.max_limit + '원' }}
      </p>

      <!-- 금리 정보 -->
      <p class="section-title">기간별 금리</p>
      <ul class="interest-list">
        <li v-for="option in saving.options" :key="option.save_trm" class="interest-item">
          <span class="term">{{ option.save_trm }}개월:</span>
          <span class="rate">{{ option.intr_rate }}% (최대 {{ option.intr_rate2 }}%)</span>
        </li>
      </ul>

      <!-- 차트 -->
      <div class="chart-container">
        <canvas id="interestChart"></canvas>
      </div>
    </div>

    <div class="button-container">
      <!-- 돌아가기 버튼 -->
      <router-link :to="{ name: 'SavingView' }" class="back-button">목록으로 돌아가기</router-link>

      <!-- 가입/제거 버튼 -->
      <button @click="handleJoin" class="join-button">
        {{ isFavorite ? '가입 해제' : '가입하기' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useFinanceStore } from '@/stores/finance';
import axios from 'axios';
import Chart from 'chart.js/auto';

const financeStore = useFinanceStore();
const saving = ref({}); // 적금 상품 정보
const isFavorite = ref(false); // 즐겨찾기 여부 상태
const route = useRoute();

// API 요청 URL
const API_URL = 'http://127.0.0.1:8000/finlife/saving-products/detail';

// 데이터 가져오기
onMounted(() => {
  const product_id = route.params.product_id; // URL에서 id 가져오기
  axios
    .get(`${API_URL}/${product_id}/`) // 상품 상세 정보 API 호출
    .then((res) => {
      console.log('데이터 가져오기 성공:', res.data);
      saving.value = res.data; // API 응답 데이터를 saving에 저장
      checkFavorite(); // 즐겨찾기 여부 확인
      drawInterestChart(); // 차트 생성
    })
    .catch((err) => {
      console.error('데이터 가져오기 실패:', err.response || err);
    });
});

// 즐겨찾기 여부 확인
const checkFavorite = async () => {
  await financeStore.fetchFavorites(); // 즐겨찾기 데이터 최신화
  isFavorite.value = financeStore.favoriteSavings.some(
    (item) => item.fin_prdt_cd === saving.value.fin_prdt_cd
  );
  console.log('현재 isFavorite 상태:', isFavorite.value); // 상태 디버깅용
};

// 금리 차트 그리기
const drawInterestChart = () => {
  const labels = saving.value.options.map(option => `${option.save_trm}개월`); // x축: 개월수
  const data = saving.value.options.map(option => option.intr_rate); // y축: 이자율

  const ctx = document.getElementById("interestChart").getContext("2d");

  new Chart(ctx, {
    type: "line", // 라인 차트
    data: {
      labels: labels,
      datasets: [
        {
          label: "금리(%)",
          data: data,
          borderColor: "#27ae60",
          backgroundColor: "rgba(39, 174, 96, 0.2)",
          fill: true,
          tension: 0.4, // 라인의 곡선 정도
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "개월 수",
          },
        },
        y: {
          title: {
            display: true,
            text: "금리 (%)",
          },
          beginAtZero: true, // y축을 0부터 시작
        },
      },
    },
  });
};

// 가입/제거 버튼 클릭 처리
const handleJoin = async () => {
  try {
    await financeStore.toggleFavoriteSaving(saving.value.fin_prdt_cd); // 즐겨찾기 토글
    isFavorite.value = !isFavorite.value; // 상태 토글
    alert(isFavorite.value ? '적금 즐겨찾기에 추가되었습니다.' : '적금 즐겨찾기에서 제거되었습니다.');
  } catch (error) {
    alert('작업 중 오류가 발생했습니다.');
    console.error('handleJoin 오류:', error.response?.data || error.message);
  }
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: #f4f6f8;
  min-height: 100vh;
}

/* 상세 정보 카드 */
.detail-card {
  background-color: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 800px;
  margin-bottom: 2rem;
  text-align: left;
}

/* 제목 스타일 */
.title {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 1rem;
}

/* 부제목 스타일 */
.subtitle {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
}

/* 섹션 제목 스타일 */
.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 1.5rem 0 1rem;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

/* 금리 목록 스타일 */
.interest-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.interest-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #ecf0f1;
  font-size: 1rem;
  color: #34495e;
}

.term {
  font-weight: bold;
}

.rate {
  color: #27ae60;
  font-weight: bold;
}

/* 버튼 컨테이너 */
.button-container {
  display: flex;
  gap: 1rem;
}

/* 돌아가기 버튼 스타일 */
.back-button {
  background-color: #3498db;
  color: #ffffff;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #2980b9;
}

/* 가입하기 버튼 스타일 */
.join-button {
  background-color: #27ae60;
  color: #ffffff;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.join-button:hover {
  background-color: #1e8449;
}

/* 차트 컨테이너 */
.chart-container {
  width: 100%;
  max-width: 600px;
  height: 400px;
  margin-top: 2rem;
}
</style>
