<template>
  <v-container class="mt-5">
    <!-- 게시글 상세 -->
    <v-card elevation="3" class="mb-4">
      <v-card-text>
        <h1 class="text-center mb-4" style="color: #3498db;">게시글 상세</h1>

        <div v-if="article && article.user">
          <!-- 작성자 -->
          <v-row class="mb-3">
            <v-col cols="3" class="fw-bold">작성자:</v-col>
            <v-col cols="9">
              <RouterLink
                :to="{ name: 'OtherUserProfile', params: { username: article.user.username } }"
                class="author-link"
              >
                {{ article.user.username }}
              </RouterLink>
            </v-col>
          </v-row>

          <!-- 제목 -->
          <v-row class="mb-3">
            <v-col cols="3" class="fw-bold">제목:</v-col>
            <v-col cols="9">{{ article.title }}</v-col>
          </v-row>

          <!-- 내용 -->
          <v-row class="mb-3">
            <v-col cols="3" class="fw-bold">내용:</v-col>
            <v-col cols="9">{{ article.content }}</v-col>
          </v-row>

          <!-- 좋아요 -->
          <v-row class="mb-3">
            <v-col cols="3" class="fw-bold">좋아요:</v-col>
            <v-col cols="9">
              <v-btn
                icon
                :color="isLikedByUser ? 'pink' : 'grey'"
                @click="toggleLike"
              >
                <template v-if="isLikedByUser">
                  <v-icon>mdi-heart</v-icon>
                </template>
                <template v-else>
                  <v-icon>mdi-heart-outline</v-icon>
                </template>
              </v-btn>
              <span>{{ article.likes_count }}개</span>
            </v-col>
          </v-row>

          <!-- 작성일 -->
          <v-row class="mb-3">
            <v-col cols="3" class="fw-bold">작성일:</v-col>
            <v-col cols="9">{{ formatDate(article.created_at) }}</v-col>
          </v-row>
        </div>

        <!-- 로딩 상태 -->
        <div v-else class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>
      </v-card-text>
    </v-card>

    <!-- 댓글 섹션 -->
    <v-card elevation="3">
      <v-card-text>
        <h5 class="text-primary mb-4">댓글</h5>
        <!-- 댓글 목록 -->
        <div v-for="comment in comments" :key="comment.id" class="mb-3">
          <p>
            <strong>{{ comment.user.username }}</strong>: {{ comment.content }}
            <small class="text-muted">({{ formatDate(comment.created_at) }})</small>
          </p>
          <div v-if="isAuthor(comment.user.username)">
            <v-btn text small @click="editComment(comment)">수정</v-btn>
            <v-btn text small color="error" @click="deleteComment(comment.id)">삭제</v-btn>
          </div>
        </div>

        <!-- 댓글 작성 -->
        <v-textarea
          v-model="newComment"
          label="댓글을 입력하세요"
          rows="2"
          outlined
          dense
        ></v-textarea>
        <v-btn class="mt-2" color="primary" large @click="addComment">
          댓글 작성
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- 뒤로가기 및 게시글 수정/삭제 -->
    <div class="mt-4 text-center">
      <v-btn color="secondary" class="me-2" @click="goBack">뒤로 가기</v-btn>
      <v-btn
        v-if="isArticleAuthor"
        color="primary"
        class="me-2"
        :to="{ name: 'UpdateView', params: { id: article.id } }"
      >
        수정하기
      </v-btn>
      <v-btn
        v-if="isArticleAuthor"
        color="error"
        @click="deleteArticle"
      >
        삭제하기
      </v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCommunityStore } from '@/stores/community'
import { useAccountStore } from '@/stores/accounts'
import { useRoute, useRouter } from 'vue-router'

const communityStore = useCommunityStore()
const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()

// 게시글 및 댓글 상태
const article = ref({})
const comments = ref([])
const newComment = ref('')
const isLikedByUser = ref(false)

// 작성자 여부 확인
const isArticleAuthor = computed(() => {
  return article.value.user?.username === accountStore.username
})

// 댓글 작성자 확인
const isAuthor = (username) => {
  return username === accountStore.username
}

// 게시글 가져오기
onMounted(() => {
  const articleId = route.params.id

  communityStore
    .getArticleDetail(articleId)
    .then((data) => {
      article.value = data.article
      comments.value = data.comments
      isLikedByUser.value = data.article.liked_by_user
    })
    .catch((err) => {
      console.error('게시글 상세 가져오기 실패:', err)
      alert('게시글 정보를 가져오는 데 실패했습니다.')
      router.push({ name: 'ArticleView' })
    })
})

// 게시글 좋아요 토글
const toggleLike = () => {
  const articleId = route.params.id

  communityStore
    .toggleLikeArticle(articleId)
    .then(() => {
      isLikedByUser.value = !isLikedByUser.value
      article.value.likes_count += isLikedByUser.value ? 1 : -1
    })
    .catch((err) => {
      console.error('좋아요 토글 실패:', err)
      alert('좋아요를 처리하는 데 실패했습니다.')
    })
}

// 게시글 삭제
const deleteArticle = () => {
  const articleId = route.params.id

  communityStore
    .deleteArticle(articleId)
    .then(() => {
      alert('게시글이 성공적으로 삭제되었습니다.')
      router.push({ name: 'ArticleView' })
    })
    .catch((err) => {
      console.error('게시글 삭제 실패:', err)
      alert('게시글 삭제에 실패했습니다.')
    })
}

// 댓글 작성
const addComment = () => {
  const articleId = route.params.id
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }
  communityStore
    .createComment(articleId, { content: newComment.value })
    .then(() => {
      newComment.value = ''
      return communityStore.getComments(articleId)
    })
    .then((data) => {
      comments.value = data
    })
    .catch((err) => {
      console.error('댓글 작성 실패:', err)
      alert('댓글 작성에 실패했습니다.')
    })
}

// 댓글 삭제
const deleteComment = (commentId) => {
  const articleId = route.params.id
  communityStore
    .deleteComment(articleId, commentId)
    .then(() => {
      return communityStore.getComments(articleId)
    })
    .then((data) => {
      comments.value = data
    })
    .catch((err) => {
      console.error('댓글 삭제 실패:', err)
      alert('댓글 삭제에 실패했습니다.')
    })
}

// 댓글 수정
const editComment = (comment) => {
  const updatedContent = prompt('댓글 내용을 수정하세요:', comment.content)
  if (updatedContent) {
    communityStore
      .updateComment(comment.id, { content: updatedContent })
      .then(() => {
        const articleId = route.params.id
        return communityStore.getComments(articleId)
      })
      .then((data) => {
        comments.value = data
      })
      .catch((err) => {
        console.error('댓글 수정 실패:', err)
        alert('댓글 수정에 실패했습니다.')
      })
  }
}

// 날짜 포맷
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleDateString('ko-KR', options)
}

// 뒤로가기
const goBack = () => {
  router.push({ name: 'ArticleView' })
}
</script>

<style scoped>
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
