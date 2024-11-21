<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="card-title text-center mb-4">게시글 수정</h1>
            <form @submit.prevent="updateArticle">
              <div class="form-group mb-3">
                <label for="title" class="form-label">제목</label>
                <input
                  type="text"
                  id="title"
                  v-model="title"
                  class="form-control"
                  required
                  placeholder="수정할 제목을 입력하세요"
                />
              </div>
              <div class="form-group mb-4">
                <label for="content" class="form-label">내용</label>
                <textarea
                  id="content"
                  v-model="content"
                  class="form-control"
                  rows="5"
                  required
                  placeholder="수정할 내용을 입력하세요"
                ></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">수정하기</button>
              </div>
              <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCommunityStore } from '@/stores/community'
import { useRoute, useRouter } from 'vue-router'

const communityStore = useCommunityStore()
const route = useRoute()
const router = useRouter()

// 상태 변수
const title = ref('')
const content = ref('')
const errorMessage = ref('')

// 게시글 불러오기
onMounted(() => {
  const articleId = route.params.id
  communityStore
    .getArticleDetail(articleId)
    .then((data) => {
      title.value = data.article.title
      content.value = data.article.content
    })
    .catch((err) => {
      console.error('게시글 가져오기 실패:', err)
      alert('게시글 정보를 불러오지 못했습니다.')
      router.push({ name: 'ArticleView' }) // 게시판으로 이동
    })
})

// 게시글 수정
const updateArticle = () => {
  const articleId = route.params.id
  const payload = {
    title: title.value,
    content: content.value,
  }

  communityStore
    .updateArticle(articleId, payload)
    .then(() => {
      alert('게시글이 성공적으로 수정되었습니다.')
      router.push({ name: 'DetailView', params: { id: articleId } }) // 상세 페이지로 이동
    })
    .catch((err) => {
      console.error('게시글 수정 실패:', err)
      errorMessage.value = '게시글 수정에 실패했습니다. 다시 시도해주세요.'
    })
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 15px;
}

.card-title {
  color: #3498db;
  font-weight: bold;
}

.form-control:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.alert-danger {
  margin-top: 10px;
}
</style>
