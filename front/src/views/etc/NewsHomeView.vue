<template>
  <div class="news-container">
    <h1 class="text-center my-4">최신 경제 뉴스</h1>

    <div v-if="loading" class="text-center">
      <p>뉴스를 불러오는 중...</p>
    </div>

    <div v-else>
      <!-- 새로고침 버튼 -->
      <div class="text-center mb-3">
        <button @click="refreshNews" class="btn btn-primary">
          <i class="fas fa-sync-alt"></i> 새로고침
        </button>
      </div>

      <!-- 뉴스 목록 -->
      <div v-for="news in newsList" :key="news.link" class="news-item mb-4">
        <img 
          v-if="news.thumbnail" 
          :src="news.thumbnail" 
          alt="뉴스 썸네일" 
          class="news-thumbnail" 
        />
        <h3>
          <a :href="news.link" target="_blank" rel="noopener noreferrer">
            {{ news.title }}
          </a>
        </h3>
        <p class="text-muted">{{ news.pub_date }}</p>
        <p>{{ news.description }}</p>
      </div>

      <!-- 페이지 네비게이션 -->
      <div class="pagination mt-4 text-center">
        <button
          class="btn btn-outline-primary me-2"
          :disabled="currentPage === 1"
          @click="fetchNews(currentPage - 1)"
        >
          이전
        </button>

        <button
          v-for="page in pageNumbers"
          :key="page"
          @click="fetchNews(page)"
          :class="['btn', 'btn-outline-primary', 'me-1', { active: page === currentPage }]"
        >
          {{ page }}
        </button>

        <button
          class="btn btn-outline-primary ms-2"
          :disabled="currentPage === totalPages"
          @click="fetchNews(currentPage + 1)"
        >
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/info/news/'

const newsList = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const loading = ref(true)

// 페이지 번호 계산 (최대 10개 표시)
const pageNumbers = computed(() => {
  const pages = []
  const start = Math.max(currentPage.value - 5, 1) // 현재 페이지에서 앞뒤로 5개
  const end = Math.min(start + 9, totalPages.value) // 총 10개까지
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const fetchNews = async (page = 1) => {
  loading.value = true
  try {
    const response = await axios.get(`${API_URL}?page=${page}`)
    if (response.status === 200) {
      newsList.value = response.data.news
      totalPages.value = response.data.total_pages
      currentPage.value = page
    } else {
      console.error('API 호출 실패:', response)
    }
  } catch (error) {
    console.error('뉴스 데이터를 가져오는 데 실패했습니다:', error)
    alert('뉴스 데이터를 가져오는 데 문제가 발생했습니다.')
  } finally {
    loading.value = false
  }
}

// 새로고침
const refreshNews = () => {
  fetchNews(currentPage.value)
}

// 초기 로드
onMounted(() => {
  fetchNews()
})
</script>

<style scoped>
.news-container {
  max-width: 800px;
  margin: 0 auto;
}

.news-item {
  border-bottom: 1px solid #ccc;
  padding-bottom: 1rem;
}

.news-thumbnail {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  margin-bottom: 0.5rem;
}

.news-item h3 {
  font-size: 1.25rem;
}

.news-item p {
  margin: 0.5rem 0;
}

.pagination .btn {
  margin: 0 0.2rem;
}

.pagination .btn.active {
  background-color: #3498db;
  color: white;
}
</style>
