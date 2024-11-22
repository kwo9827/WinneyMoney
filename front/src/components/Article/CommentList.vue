<template>
  <div class="mt-4">
    <h5 class="text-primary">댓글</h5>
    <div v-for="comment in comments" :key="comment.id" class="mb-3">
      <CommentListItem 
      :comment="comment" 
      :isAuthor="comment.user.username === currentUser" />
    </div>
    <form @submit.prevent="addComment" class="mt-4">
      <textarea
        v-model="newComment"
        placeholder="댓글을 작성하세요"
        class="form-control"
        rows="2"
        required
      ></textarea>
      <button type="submit" class="btn btn-primary mt-2">댓글 작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import { useAccountStore } from '@/stores/accounts'
import CommentListItem from '@/components/Article/CommentListItem.vue'

const communityStore = useCommunityStore()
const accountStore = useAccountStore()
const route = useRoute()

// 상태 변수
const comments = ref([])
const newComment = ref('')

// 현재 로그인한 사용자 이름
const currentUser = accountStore.username

// 현재 게시글 ID
const articleId = route.params.id

// 댓글 가져오기
const fetchComments = () => {
  communityStore
    .getComments(articleId)
    .then((data) => {
      comments.value = data
    })
    .catch((err) => {
      console.error('댓글 가져오기 실패:', err)
    })
}

// 댓글 작성
const addComment = () => {
  const payload = { content: newComment.value }

  communityStore
    .createComment(articleId, payload)
    .then(() => {
      newComment.value = ''
      fetchComments() // 댓글 작성 후 댓글 리스트 새로고침
    })
    .catch((err) => {
      console.error('댓글 작성 실패:', err)
    })
}

// 컴포넌트 마운트 시 댓글 가져오기
onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
h5 {
  font-weight: bold;
  margin-bottom: 1rem;
}
</style>
