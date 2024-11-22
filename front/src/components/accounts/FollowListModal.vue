<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">
        {{ type === 'followers' ? '팔로워 목록' : '팔로잉 목록' }}
      </h3>
      <ul class="list-group">
        <li
          v-for="user in list"
          :key="user.username"
          class="list-group-item"
        >
          <strong>{{ user.username }}</strong> ({{ user.name }})
        </li>
      </ul>
      <button class="btn btn-secondary mt-3" @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: String, // 'followers' 또는 'following'
  list: Array, // 사용자 리스트
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  width: 90%;
  text-align: center;
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.list-group-item {
  text-align: left;
}
</style>
