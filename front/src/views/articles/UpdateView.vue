<template>
  <v-container class="mt-5">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card elevation="3">
          <v-card-text>
            <h1 class="text-center mb-4" style="color: #3498db;">게시글 수정</h1>
            <v-form @submit.prevent="updateArticle">
              <!-- 제목 입력 -->
              <v-text-field
                v-model="title"
                label="제목"
                placeholder="수정할 제목을 입력하세요"
                outlined
                dense
                required
              ></v-text-field>

              <!-- 내용 입력 -->
              <v-textarea
                v-model="content"
                label="내용"
                placeholder="수정할 내용을 입력하세요"
                rows="5"
                outlined
                dense
                required
              ></v-textarea>

              <!-- 제출 버튼 -->
              <div class="d-grid mt-4">
                <v-btn color="primary" large elevation="2" type="submit">
                  수정하기
                </v-btn>
              </div>

              <!-- 에러 메시지 -->
              <v-alert
                v-if="errorMessage"
                type="error"
                class="mt-3"
                border="left"
                prominent
              >
                {{ errorMessage }}
              </v-alert>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
.v-card {
  border-radius: 15px;
  padding: 2rem;
}

.text-center {
  color: #3498db;
  font-weight: bold;
}

.v-btn {
  transition: all 0.3s ease;
}

.v-btn:hover {
  background-color: #2980b9 !important;
}

.v-alert {
  margin-top: 10px;
}
</style>
