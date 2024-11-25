<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">회원정보 변경</h2>
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label for="email" class="form-label">이메일</label>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="firstName" class="form-label">이름</label>
                <input
                  type="text"
                  id="firstName"
                  v-model="firstName"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="lastName" class="form-label">성</label>
                <input
                  type="text"
                  id="lastName"
                  v-model="lastName"
                  class="form-control"
                  required
                />
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">정보 수정</button>
              </div>
              <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
              </div>
            </form>
            <!-- 비밀번호 변경 및 찾기 링크 -->
            <div class="mt-4 text-center">
              <RouterLink :to="{ name: 'ChangePasswordView' }" class="btn-link">
                비밀번호 변경
              </RouterLink>
              <!-- <span> | </span>
              <RouterLink :to="{ name: 'FindPasswordView' }" class="btn-link">
                비밀번호 찾기
              </RouterLink> -->
            </div>
            <!-- 뒤로가기 버튼 -->
            <div class="mt-4 text-center">
              <button class="btn btn-secondary" @click="goBack">뒤로 가기</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const store = useAccountStore()
const router = useRouter()

// 상태 변수
const email = ref('')
const firstName = ref('')
const lastName = ref('')
const errorMessage = ref('')

// 사용자 프로필 로드
onMounted(() => {
  store.getUserProfile().then(() => {
    email.value = store.email
    firstName.value = store.firstName
    lastName.value = store.lastName
  })
})

// 프로필 업데이트
const updateProfile = () => {
  const payload = {
    email: email.value,
    first_name: firstName.value,
    last_name: lastName.value,
  }

  store
    .updateProfile(payload)
    .then(() => {
      alert('회원정보가 성공적으로 변경되었습니다.')
    })
    .catch((err) => {
      console.error('회원정보 변경 실패:', err)
      errorMessage.value = '회원정보 변경에 실패했습니다. 다시 시도해주세요.'
    })
}

// 뒤로 가기 기능
const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.container {
  margin-top: 50px;
}

.card {
  border: none;
  border-radius: 1rem;
  transition: all 0.2s;
  background-color: #ffffff;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175);
}

.card-title {
  color: #2c3e50;
  font-weight: bold;
  font-size: 1.5rem;
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  font-size: 1rem;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.alert-danger {
  margin-top: 10px;
  font-size: 0.9rem;
}

.btn-link {
  color: #3498db;
  text-decoration: none;
  font-size: 0.9rem;
}

.btn-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.btn-secondary {
  background-color: #95a5a6;
  border-color: #95a5a6;
  color: #ffffff;
  font-size: 1rem;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
  border-color: #7f8c8d;
}
</style>
