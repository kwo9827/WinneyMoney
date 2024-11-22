<template>
  <v-container class="fill-height welcome-container" fluid>
    <v-row align="center" justify="center" class="text-center">
      <v-col cols="12" md="8">
        <h1 class="title">WinneyMoney</h1>
        <p class="subtitle">당신의 스마트한 금융 파트너</p>
        <h2 class="welcome-message">환영합니다!</h2>
        <p class="description">
          WinneyMoney와 함께 지금 당장 시작하세요.
        </p>
        <div class="cta-buttons">
          <v-btn color="success" large class="me-3" elevation="2">
            자신에게 맞는 금융 상품 알아보기
          </v-btn>
          <v-btn outlined color="white" large elevation="2">
            예금, 적금 상품 담으러가기
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
</script>

<style scoped>
.welcome-container {
  background: linear-gradient(135deg, #3498db, #8e44ad);
  color: white;
  padding: 20px;
}

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

.cta-buttons {
  margin-top: 2rem;
}

.v-btn {
  transition: all 0.3s ease;
}

.v-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

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
}
</style>
