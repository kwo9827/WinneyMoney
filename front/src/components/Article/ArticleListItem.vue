<template>
  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">{{ article.title }}</h5>
        <!--작성자 이름 클릭 시 프로필로 이동-->
        <h6 class="card-subtitle mb-2 text-muted">
          작성자: 
          <RouterLink
            v-if="article.user"
            :to="{ name: 'OtherUserProfile', params: { username: article.user.username } }"
            class="author-link"
          >
            {{ article.user.username }}
          </RouterLink>
          <span v-else>알 수 없음</span>
        </h6>
        <p class="card-text">{{ truncateContent(article.content) }}</p>
      </div>
      <div class="card-footer bg-transparent border-top-0">
        <RouterLink
          v-if="article.id"
          :to="{ name: 'DetailView', params: { id: article.id } }"
          class="btn btn-outline-primary btn-sm"
        >
          상세보기
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})

const truncateContent = (content) => {
  return content.length > 100 ? content.slice(0, 100) + '...' : content
}
</script>

<style scoped>
.card {
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}

.card-title {
  font-weight: bold;
  color: #2c3e50;
}

.card-text {
  color: #34495e;
}

.btn-outline-primary {
  border-color: #3498db;
  color: #3498db;
}

.btn-outline-primary:hover {
  background-color: #3498db;
  color: white;
}

/* 작성자 링크 스타일 */
.author-link {
  text-decoration: none;
  color: #3498db;
  font-weight: bold;
}

.author-link:hover {
  text-decoration: underline;
  color: #2980b9;
}
</style>
