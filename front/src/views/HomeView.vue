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
        <button class="btn btn-primary btn-lg me-3">자신에게 맞는 금융 상품 알아보기</button>
        <button class="btn btn-outline-primary btn-lg">예금, 적금 상품 담으러가기</button>
      </div>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.welcome-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #3498db, #8e44ad);
  color: white;
  text-align: center;
  padding: 20px;
}

.content {
  max-width: 800px;
}

.title {
  font-size: 4rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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

.btn-primary {
  background-color: #2ecc71;
  border-color: #2ecc71;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #27ae60;
  border-color: #27ae60;
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-outline-primary {
  color: white;
  border-color: white;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: white;
  color: #3498db;
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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