<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="card-title text-center mb-4">게시글 작성</h1>
            <form @submit.prevent="createArticle">
              <div class="form-group mb-3">
                <label for="title" class="form-label">제목</label>
                <input 
                  type="text" 
                  id="title" 
                  v-model.trim="title" 
                  class="form-control" 
                  required 
                  placeholder="제목을 입력하세요" 
                />
              </div>
              <div class="form-group mb-4">
                <label for="content" class="form-label">내용</label>
                <textarea 
                  id="content" 
                  v-model.trim="content" 
                  class="form-control" 
                  rows="5" 
                  required 
                  placeholder="내용을 입력하세요"
                ></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">게시글 작성</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCommunityStore } from '@/stores/community'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

// 상태 변수
const title = ref('')
const content = ref('')
const communityStore = useCommunityStore()
const accountStore = useAccountStore()
const router = useRouter()

// 게시글 생성 핸들러
const createArticle = function () {
  const payload = {
    title: title.value,
    content: content.value,
  }
  const token = accountStore.token

  if (!token) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'LogInView' })
    return
  }

  communityStore.createArticle(payload, token)
    .then(() => {
      alert('게시글이 성공적으로 생성되었습니다.')
      router.push({ name: 'ArticleView' }) // 게시판으로 이동
    })
    .catch((err) => {
      alert('게시글 생성에 실패했습니다. 다시 시도해주세요.')
      console.error('게시글 생성 실패:', err)
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
</style>
