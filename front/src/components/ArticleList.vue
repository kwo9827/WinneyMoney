<template>
  <div class="container mt-4">
    <h3 class="mb-4 text-center">유저 게시판</h3>
    <div class="row" v-if="store.articles">
      <ArticleListItem 
        v-for="article in store.articles"
        :key="article.id"
        :article="article"
      />
    </div>
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { useCommunityStore } from '@/stores/community'

const store = useCommunityStore()
</script>

<style scoped>
h3 {
  color: #2c3e50;
  font-weight: bold;
}
</style>