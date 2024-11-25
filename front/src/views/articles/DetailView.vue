<template>
  <div class="container mt-5">
    <!-- 게시글 상세 -->
    <div class="card mb-4">
      <div class="card-body">
        <h1 class="text-center mb-4" style="color: #3498db;">게시글 상세</h1>

        <div v-if="article && article.user">
          <!-- 작성자 -->
          <div class="row mb-3">
            <div class="col-3 fw-bold">작성자:</div>
            <div class="col-9">
              <router-link
                :to="{ name: 'OtherUserProfile', params: { username: article.user.username } }"
                class="author-link"
              >
                {{ article.user.username }}
              </router-link>
            </div>
          </div>

          <!-- 제목 -->
          <div class="row mb-3">
            <div class="col-3 fw-bold">제목:</div>
            <div class="col-9">{{ article.title }}</div>
          </div>

          <!-- 내용 -->
          <div class="row mb-3">
            <div class="col-3 fw-bold">내용:</div>
            <div class="col-9">{{ article.content }}</div>
          </div>

          <!-- 좋아요 -->
          <div class="row mb-3">
            <div class="col-3 fw-bold">좋아요:</div>
            <div class="col-9">
              <button class="like-btn" @click="toggleLike">
                <span v-if="isLikedByUser" class="like-icon liked">♥</span>
                <span v-else class="like-icon">♡</span>
              </button>
              <span class="like-count">{{ article.likes_count }}개</span>
            </div>
          </div>

          <!-- 작성일 -->
          <div class="row mb-3">
            <div class="col-3 fw-bold">작성일:</div>
            <div class="col-9">{{ formatDate(article.created_at) }}</div>
          </div>
        </div>

        <!-- 로딩 상태 -->
        <div v-else class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 댓글 섹션 -->
    <div class="card">
      <div class="card-body">
        <h5 class="text-primary mb-4">댓글</h5>

        <!-- 댓글 목록 -->
        <div v-for="comment in comments" :key="comment.id" class="mb-3">
          <p>
            <strong>{{ comment.user.username }}</strong>: {{ comment.content }}
            <small class="text-muted">({{ formatDate(comment.created_at) }})</small>
          </p>
          <div v-if="isAuthor(comment.user.username)">
            <button class="btn btn-link p-0 me-2" @click="editComment(comment)">수정</button>
            <button class="btn btn-link text-danger p-0" @click="deleteComment(comment.id)">삭제</button>
          </div>
        </div>

        <!-- 댓글 작성 -->
        <textarea
          v-model="newComment"
          class="form-control"
          placeholder="댓글을 입력하세요"
          rows="2"
        ></textarea>
        <button class="btn btn-primary mt-2" @click="addComment">댓글 작성</button>
      </div>
    </div>

    <!-- 뒤로가기 및 게시글 수정/삭제 -->
    <div class="mt-4 text-center">
      <button class="btn btn-secondary me-2" @click="goBack">뒤로 가기</button>
      <button
        v-if="isArticleAuthor"
        class="btn btn-primary me-2"
        @click="$router.push({ name: 'UpdateView', params: { id: article.id } })"
      >
        수정하기
      </button>
      <button
        v-if="isArticleAuthor"
        class="btn btn-danger"
        @click="deleteArticle"
      >
        삭제하기
      </button>
    </div>
  </div>
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

const article = ref({})
const comments = ref([])
const newComment = ref('')
const isLikedByUser = ref(false)

const isArticleAuthor = computed(() => {
  return article.value.user?.username === accountStore.username
})

const isAuthor = (username) => {
  return username === accountStore.username
}

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

const toggleLike = () => {
  const articleId = route.params.id

  communityStore
    .toggleLikeArticle(articleId)
    .then(() => {
      isLikedByUser.value = !isLikedByUser.value
      article.value.likes_count += isLikedByUser.value ? 1 : -1
    })
    .catch((err) => {
      console.error('좋아요 처리 실패:', err)
      alert('좋아요 처리에 실패했습니다.')
    })
}

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

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleDateString('ko-KR', options)
}

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

.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 0;
}

.like-btn .like-icon {
  font-size: 2rem;
  color: grey;
  transition: color 0.3s ease;
}

.like-btn .like-icon.liked {
  color: red;
}

.like-count {
  margin-left: 8px;
  font-size: 1rem;
  color: #555;
}
</style>
