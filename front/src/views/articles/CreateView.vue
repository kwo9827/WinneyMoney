<template>
  <v-container class="mt-5">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card elevation="3">
          <v-card-text>
            <h1 class="text-center mb-4" style="color: #3498db;">게시글 작성</h1>
            <v-form @submit.prevent="createArticle">
              <!-- 제목 입력 -->
              <v-text-field
                v-model.trim="title"
                label="제목"
                placeholder="제목을 입력하세요"
                outlined
                dense
                required
              ></v-text-field>

              <!-- 내용 입력 -->
              <v-textarea
                v-model.trim="content"
                label="내용"
                placeholder="내용을 입력하세요"
                rows="5"
                outlined
                dense
                required
              ></v-textarea>

              <!-- 제출 버튼 -->
              <div class="d-grid mt-4">
                <v-btn
                  color="primary"
                  large
                  elevation="2"
                  type="submit"
                >
                  게시글 작성
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
.text-center {
  color: #3498db;
  font-weight: bold;
}

.v-text-field, .v-textarea {
  margin-bottom: 1.5rem;
}

.v-btn {
  background-color: #3498db;
  transition: all 0.3s ease;
}

.v-btn:hover {
  background-color: #2980b9;
}

.v-card {
  border-radius: 15px;
  padding: 2rem;
}

@media (max-width: 768px) {
  .v-card {
    padding: 1rem;
  }
}
</style>
