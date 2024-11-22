<template>
<div class="container mt-5">
    <!-- 게시글 상세 -->
    <div class="card shadow mb-4">
      <div class="card-body">
        <h1 class="card-title text-center mb-4">게시글 상세</h1>

        <div v-if="article && article.user" class="article-details">
          <div class="row mb-3">
            <div class="col-md-3 fw-bold">작성자:</div>
            <div class="col-md-9">
              <RouterLink
                :to="{ name: 'OtherUserProfile', params: { username: article.user.username } }"
                class="author-link"
              >
                {{ article.user.username }}
              </RouterLink>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-md-3 fw-bold">제목:</div>
            <div class="col-md-9">{{ article.title }}</div>
          </div>
          <div class="row mb-3">
            <div class="col-md-3 fw-bold">내용:</div>
            <div class="col-md-9">{{ article.content }}</div>
          </div>
          <div class="row mb-3">
            <div class="col-md-3 fw-bold">좋아요:</div>
            <div class="col-md-9">
              <button
                class="btn btn-outline-primary"
                @click="toggleLike"
              >
                {{ isLikedByUser ? '❤' : '🤍' }}
              </button>
              <span>{{ article.likes_count }}개</span>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-md-3 fw-bold">작성일:</div>
            <div class="col-md-9">{{ formatDate(article.created_at) }}</div>
          </div>
        </div>
        <div v-else class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 댓글 섹션 -->
    <div class="card shadow">
      <div class="card-body">
        <h5 class="text-primary mb-4">댓글</h5>
        <!-- 댓글 목록 -->
        <div v-for="comment in comments" :key="comment.id" class="mb-3">
          <p>
            <strong>{{ comment.user.username }}</strong>: {{ comment.content }}
            <small class="text-muted">({{ formatDate(comment.created_at) }})</small>
          </p>
          <div v-if="isAuthor(comment.user.username)">
            <button @click="editComment(comment)" class="btn btn-link">수정</button>
            <button @click="deleteComment(comment.id)" class="btn btn-link text-danger">삭제</button>
          </div>
        </div>

        <!-- 댓글 작성 -->
        <textarea
          v-model="newComment"
          class="form-control"
          rows="2"
          placeholder="댓글을 입력하세요"
        ></textarea>
        <button @click="addComment" class="btn btn-primary mt-2">댓글 작성</button>
      </div>
    </div>

    <!-- 뒤로가기 및 게시글 수정/삭제 -->
    <div class="mt-4 text-center">
      <button @click="goBack" class="btn btn-secondary me-2">뒤로 가기</button>
      <RouterLink
        v-if="isArticleAuthor"
        :to="{ name: 'UpdateView', params: { id: article.id } }"
        class="btn btn-primary"
      >
        수정하기
      </RouterLink>
      <button v-if="isArticleAuthor" @click="deleteArticle" class="btn btn-danger">삭제하기</button>
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
  const articleId = route.params.id;
  console.log('현재 게시글 ID:', articleId);

  communityStore
    .getArticleDetail(articleId)
    .then((data) => {
      article.value = data.article;
      comments.value = data.comments;
      isLikedByUser.value = data.article.liked_by_user; // 좋아요 상태 반영
    })
    .catch((err) => {
      console.error('게시글 상세 가져오기 실패:', err);
      alert('게시글 정보를 가져오는 데 실패했습니다.');
      router.push({ name: 'ArticleView' }); // 게시판으로 이동
    });
});

// 게시글 좋아요 토글
const toggleLike = () => {
  const articleId = route.params.id;

  communityStore
    .toggleLikeArticle(articleId)
    .then(() => {
      isLikedByUser.value = !isLikedByUser.value; // 좋아요 상태 업데이트
      article.value.likes_count += isLikedByUser.value ? 1 : -1; // 좋아요 수 업데이트
    })
    .catch((err) => {
      console.error('좋아요 토글 실패:', err);
      alert('좋아요를 처리하는 데 실패했습니다.');
    });
};

// 게시글 삭제
const deleteArticle = () => {
  const articleId = route.params.id;

  communityStore
    .deleteArticle(articleId)
    .then(() => {
      alert('게시글이 성공적으로 삭제되었습니다.');
      router.push({ name: 'ArticleView' }); // 게시판으로 이동
    })
    .catch((err) => {
      console.error('게시글 삭제 실패:', err);
      alert('게시글 삭제에 실패했습니다.');
    });
};

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
.card {
  border-radius: 15px;
}

.card-title {
  color: #3498db;
  font-weight: bold;
}

textarea {
  resize: none;
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
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
