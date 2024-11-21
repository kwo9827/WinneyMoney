<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">비밀번호 찾기</h2>
            <form @submit.prevent="sendResetEmail">
              <div class="mb-3">
                <label for="email" class="form-label">이메일</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model.trim="email" 
                  class="form-control input-lg" 
                  required
                />
              </div>
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">비밀번호 재설정 이메일 보내기</button>
              </div>
              <div class="mt-4 text-center">
                <button class="btn btn-secondary" @click="goBack">뒤로 가기</button>
              </div>
            </form>
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

const email = ref('')
const errorMessage = ref('')

const store = useAccountStore()
const router = useRouter()

// 비밀번호 재설정 이메일 전송
const sendResetEmail = function () {
  store.resetPassword(email.value)
    .then(() => {
      errorMessage.value = ''
      alert('비밀번호 재설정 이메일이 전송되었습니다. 이메일을 확인해주세요.')
    })
    .catch((err) => {
      errorMessage.value = '이메일 전송에 실패했습니다. 다시 시도해주세요.'
      console.error('비밀번호 재설정 실패:', err)
    })
}

// 뒤로 가기
const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.container {
  max-width: 500px; /* 컨테이너 크기를 넓힘 */
  margin: 0 auto;
}

.card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.6rem;
}

.form-label {
  font-weight: bold;
}

.form-control {
  font-size: 1.1rem; /* 입력창 폰트 크기 */
  padding: 12px; /* 입력창 안쪽 여백 */
  height: 48px; /* 입력창 높이 */
  border-radius: 8px; /* 입력창 모서리 둥글게 */
}

.btn-primary {
  background-color: #3b82f6;
  border: none;
  font-size: 1.1rem;
  padding: 10px;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-primary:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: #95a5a6;
  border: none;
  color: #fff;
  font-size: 1rem;
  padding: 10px;
  margin-top: 15px;
  border-radius: 8px;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
  transform: translateY(-2px);
}

.alert-danger {
  margin-top: 10px;
  font-size: 0.9rem;
  padding: 10px;
  border-radius: 8px;
}
</style>
