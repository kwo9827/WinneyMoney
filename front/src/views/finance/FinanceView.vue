<template>
  <div class="finance-container">
    <!-- 네비게이션 바 -->
    <nav class="nav-bar">
      <RouterLink
        :to="{ name: 'DepositView' }"
        class="nav-link"
        :class="{ active: $route.name === 'DepositView' }"
        @click="hideSections"
      >
        예금
      </RouterLink>
      <RouterLink
        :to="{ name: 'SavingView' }"
        class="nav-link"
        :class="{ active: $route.name === 'SavingView' }"
        @click="hideSections"
      >
        적금
      </RouterLink>
    </nav>

    <!-- 페이지 설명 및 FAQ 섹션 (조건부 렌더링) -->
    <div v-if="showSections">
      <!-- 페이지 설명 섹션 -->
      <section class="page-description">
        <h2>금융 상품 비교 서비스</h2>
        <p>
          WinneyMoney를 통해 예금 및 적금 상품을 비교하고, 최고의 금융 조건을 찾아보세요.
          카카오 지도 API를 활용하여 가까운 은행 위치를 확인할 수도 있습니다.
        </p>
      </section>

      <!-- FAQ 섹션 -->
      <section class="faq">
        <h2>💬자주 묻는 질문</h2>
        <div class="faq-item">
          <h3>어떻게 상품을 비교하나요?</h3>
          <p>상단 메뉴에서 '예금' 또는 '적금'을 선택하여 상품을 비교할 수 있습니다.</p>
        </div>
        <div class="faq-item">
          <h3>추천 서비스는 무엇인가요?</h3>
          <p>
            WinneyMoney는 사용자의 입력 정보를 기반으로 최적의 금융 상품을 추천합니다.
          </p>
        </div>
        <div class="faq-item">
          <h3>은행 위치는 어떻게 확인하나요?</h3>
          <p>서비스 메뉴에서 '은행 위치'를 선택하면 가까운 은행 지점을 확인할 수 있습니다.</p>
        </div>
      </section>
    </div>

    <!-- 메인 컨텐츠 -->
    <RouterView />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { useFinanceStore } from '@/stores/finance';

// 설명 및 FAQ 섹션 표시 여부 관리
const showSections = ref(true);

// 섹션 숨기기 함수
const hideSections = () => {
  showSections.value = false;
};

// Pinia 스토어 사용
const financeStore = useFinanceStore();

// 컴포넌트 로드 시 데이터 가져오기
onMounted(async () => {
  try {
    await financeStore.fetchDeposits(); // 예금 데이터 가져오기
    await financeStore.fetchSavings(); // 적금 데이터 가져오기
    console.log('예금 및 적금 데이터를 성공적으로 로드했습니다.');
  } catch (error) {
    console.error('데이터 로드 실패:', error);
  }
});
</script>

<style scoped>
.finance-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f4f6f8;
}

/* 네비게이션 바 스타일 */
.nav-bar {
  padding: 1rem 2rem;
  background-color: #3498db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-link {
  color: #ffffff;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0 1.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.3s, transform 0.2s;
}

.nav-link:hover {
  background-color: #2980b9;
  transform: scale(1.1);
}

.nav-link.active {
  background-color: #1f618d;
  color: #ffffff;
}

/* 페이지 설명 섹션 */
.page-description {
  text-align: center;
  margin: 2rem auto;
  padding: 1rem;
  max-width: 800px;
  color: #34495e;
}

.page-description h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.page-description p {
  font-size: 1.2rem;
  line-height: 1.6;
}

/* FAQ 섹션 */
.faq {
  background-color: #f9f9f9;
  padding: 2rem;
  border-radius: 1rem;
  margin: 2rem auto;
  max-width: 800px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.faq h2 {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

.faq-item {
  margin-bottom: 1rem;
}

.faq-item h3 {
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
  color: #3498db;
}

.faq-item p {
  font-size: 1rem;
  color: #34495e;
}

/* 메인 컨텐츠 스타일 */
.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 1rem;
  margin: 1rem auto;
  max-width: 1200px;
}
</style>
