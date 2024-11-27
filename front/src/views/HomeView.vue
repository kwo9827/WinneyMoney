<template>
  <div class="welcome-container">
    <div class="content">
      <h1 class="title">WinneyMoney</h1>
      <p class="subtitle">당신의 스마트한 금융 파트너</p>
      <h2 class="welcome-message">환영합니다!</h2>
      <p class="description">
        WinneyMoney와 함께 지금 당장 시작하세요.
      </p>
      <div class="cta-buttons">
        <router-link to="/portfolio/create" class="btn btn-success">
          자신에게 맞는 금융 상품 알아보기
        </router-link>

        <RouterLink :to="{ name: 'FinanceView' }" class="btn btn-outline">
          예금, 적금 상품 담으러가기
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
/* 전체 화면 꽉 채우기 */
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #3498db, #8e44ad);
  color: white;
  text-align: center;
}

/* 콘텐츠 스타일 */
.content {
  max-width: 800px;
  padding: 20px;
}

/* 제목 스타일 */
.title {
  font-size: 4rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  opacity: 0.8;
}

.welcome-message {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.description {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* 버튼 스타일 */
.cta-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.8rem 2rem;
  font-size: 1.2rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-success {
  background-color: #27ae60;
  color: white;
}

.btn-success:hover {
  background-color: #219150;
}

.btn-outline {
  background-color: transparent;
  color: white;
  border: 2px solid white;
}

.btn-outline:hover {
  background-color: white;
  color: #8e44ad;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .title {
    font-size: 3rem;
  }

  .subtitle {
    font-size: 1.2rem;
  }

  .welcome-message {
    font-size: 2rem;
  }

  .description {
    font-size: 1rem;
  }

  .btn {
    font-size: 1rem;
  }
}
</style>
