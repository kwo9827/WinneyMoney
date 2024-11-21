<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">로그인</h2>
            <form @submit.prevent="logIn">
              <div class="mb-3">
                <label for="username" class="form-label">사용자 이름</label>
                <input 
                  type="text" 
                  id="username" 
                  v-model.trim="username" 
                  class="form-control" 
                  required
                  autocomplete="username"
                >
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">비밀번호</label>
                <input 
                  type="password" 
                  id="password" 
                  v-model.trim="password" 
                  class="form-control" 
                  required
                  autocomplete="current-password"
                >
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">로그인</button>
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

const username = ref('')
const password = ref('')

const store = useAccountStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 1rem;
  transition: all 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
}

.card-title {
  color: #2c3e50;
  font-weight: bold;
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.form-control:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}
</style>
