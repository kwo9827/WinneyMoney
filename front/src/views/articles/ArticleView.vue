<template>
  <v-container class="mt-5 py-5" elevation="2">
    <!-- 헤더 섹션 -->
    <div class="text-center mb-4">
      <h1 class="display-4 text-primary">WinneyMoney</h1>
      <p class="lead">우리는 승승장구</p>
    </div>

    <!-- 글 작성 버튼 -->
    <div class="text-center mb-4">
      <v-btn color="primary" large class="btn-lg" :to="{ name: 'CreateView' }" elevation="2">
        <v-icon left>mdi-plus-circle</v-icon> 글 작성하기
      </v-btn>
    </div>

    <!-- 게시글 리스트 -->
    <v-row>
      <ArticleList :articles="store.articles" />
    </v-row>
  </v-container>
</template>

<script setup>
import ArticleList from '@/components/Article/ArticleList.vue'
import { onMounted } from 'vue'
import { useCommunityStore } from '@/stores/community'

const store = useCommunityStore()

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.display-4 {
  font-weight: bold;
  color: #3498db;
}

.lead {
  color: #7f8c8d;
}

.v-btn {
  transition: all 0.3s ease;
}

.v-btn:hover {
  transform: translateY(-1px);
}

.v-container {
  background-color: #f8f9fa;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .v-container {
    padding: 1rem;
  }

  .display-4 {
    font-size: 2.5rem;
  }
}
</style>
