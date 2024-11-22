<template>
  <div class="comment-item">
    <p class="fw-bold">
    <RouterLink v-if="comment.user"
    :to="{ name: 'OtherUserProfile', params: { username: comment.user.username } }">
      {{ comment.user.username }}
    </RouterLink>
    </p>
    <p>{{ comment.content }}</p>
    <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
    <button
      v-if="isAuthor"
      @click="removeComment"
      class="btn btn-link text-danger p-0"
    >
      삭제
    </button>
  </div>
</template>

<script setup>
import { useCommunityStore } from '@/stores/community'
import OtherUserProfile from '@/views/accounts/OtherUserProfile.vue';

const props = defineProps({
  comment: Object,
  isAuthor: Boolean,
})

const communityStore = useCommunityStore()

const removeComment = () => {
  communityStore.deleteComment(props.comment.id).catch((err) => {
    console.error('댓글 삭제 실패:', err)
  })
}

// 날짜 포맷
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleDateString('ko-KR', options)
}
</script>

<style scoped>
.comment-item {
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
