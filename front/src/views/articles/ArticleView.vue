<template>
  <div class="container mt-5">
    <div class="header text-center mb-4">
      <h1 class="display-4 text-primary">WinneyMoney</h1>
      <p class="lead">우리는 승승장구</p>
    </div>
    <div class="text-center mb-4">
      <RouterLink :to="{ name: 'CreateView' }" class="btn btn-primary btn-lg">
        <i class="fas fa-plus-circle me-2"></i>글 작성하기
      </RouterLink>
    </div>
    <div class="row">
      <ArticleList :articles="store.articles" />
    </div>
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted } from 'vue'
import { useCommunityStore } from '@/stores/community'

const store = useCommunityStore()

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.header {
  margin-bottom: 2rem;
}

.display-4 {
  font-weight: bold;
  color: #3498db;
}

.lead {
  color: #7f8c8d;
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
  
  .display-4 {
    font-size: 2.5rem;
  }
}
</style>
