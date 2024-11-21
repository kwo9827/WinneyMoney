<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">비밀번호 변경</h2>
            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label for="old_password" class="form-label">현재 비밀번호</label>
                <input 
                  type="password" 
                  id="old_password" 
                  v-model.trim="oldPassword" 
                  class="form-control input-lg" 
                  required
                />
              </div>
              <div class="mb-3">
                <label for="new_password1" class="form-label">새 비밀번호</label>
                <input 
                  type="password" 
                  id="new_password1" 
                  v-model.trim="newPassword1" 
                  class="form-control input-lg" 
                  required
                />
              </div>
              <div class="mb-3">
                <label for="new_password2" class="form-label">새 비밀번호 확인</label>
                <input 
                  type="password" 
                  id="new_password2" 
                  v-model.trim="newPassword2" 
                  class="form-control input-lg" 
                  required
                />
              </div>
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">비밀번호 변경</button>
              </div>
            </form>
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
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const oldPassword = ref('')
const newPassword1 = ref('')
const newPassword2 = ref('')
const errorMessage = ref('')

const store = useAccountStore()
const router = useRouter()

// 비밀번호 변경
const changePassword = function () {
  const payload = {
    old_password: oldPassword.value,
    new_password1: newPassword1.value,
    new_password2: newPassword2.value,
  }

  store.changePassword(payload)
    .then(() => {
      alert('비밀번호가 성공적으로 변경되었습니다.')
      router.push({ name: 'ProfileView' })
    })
    .catch((err) => {
      errorMessage.value = '비밀번호 변경에 실패했습니다. 다시 시도해주세요.'
      console.error('비밀번호 변경 실패:', err)
    })
}

// 뒤로 가기
const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.container {
  max-width: 500px; /* 컨테이너의 너비를 넓힘 */
  margin: 0 auto;
}

.card {
  border-radius: 10px;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175);
}

.card-title {
  font-weight: bold;
  color: #3b82f6;
  font-size: 1.5rem;
}

.form-label {
  font-weight: bold;
}

.form-control {
  font-size: 1.1rem; /* 입력창 폰트 크기 */
  padding: 12px; /* 입력창 안쪽 여백 조정 */
  height: 45px; /* 입력창 높이 */
}

.btn-primary {
  background-color: #3b82f6;
  border: none;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.alert-danger {
  margin-top: 10px;
}

.btn-secondary {
  background-color: #95a5a6;
  border-color: #95a5a6;
  color: #ffffff;
  font-size: 1rem;
  margin-top: 15px;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
  border-color: #7f8c8d;
}
</style>
