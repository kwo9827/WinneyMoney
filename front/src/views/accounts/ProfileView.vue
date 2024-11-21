<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">사용자 프로필</h2>
            <!-- 프로필 이미지 -->
            <div class="text-center mb-4">
              <img 
                :src="store.profileImage || 'https://via.placeholder.com/150'" 
                alt="프로필 이미지" 
                class="rounded-circle profile-image"
              >
            </div>
            <!-- 사용자 정보 -->
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <strong>사용자명:</strong> {{ store.username }}
              </li>
              <li class="list-group-item">
                <strong>이메일:</strong> {{ store.email }}
              </li>
              <li class="list-group-item">
                <strong>이름:</strong> {{ store.lastName }}{{ store.firstName }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const store = useAccountStore()

// 컴포넌트 마운트 시 사용자 프로필 정보를 가져옴
onMounted(() => {
  store.getUserProfile()
})
</script>

<style scoped>
/* 카드 스타일 */
.card {
  border: none;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* 프로필 이미지 스타일 */
.profile-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border: 3px solid #3498db;
}

/* 카드 제목 스타일 */
.card-title {
  color: #2c3e50;
  font-weight: bold;
}

/* 리스트 그룹 스타일 */
.list-group-item {
  font-size: 1rem;
  color: #2c3e50;
  border: none;
  padding: 0.75rem 1.25rem;
}

.list-group-item:not(:last-child) {
  border-bottom: 1px solid #f1f1f1;
}

/* 호버 효과 */
.list-group-item:hover {
  background-color: #f9f9f9;
}

/* 버튼 스타일 */
.btn-link {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

.btn-link:hover {
  color: #2980b9;
  text-decoration: underline;
}
</style>
