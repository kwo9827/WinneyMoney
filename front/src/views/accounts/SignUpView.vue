<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">회원가입</h2>
            <form @submit.prevent="handleSignUp">
              <div class="mb-3">
                <label for="username" class="form-label">아이디</label>
                <input
                  type="text"
                  id="username"
                  v-model.trim="username"
                  class="form-control"
                  required
                  autocomplete="username"
                />
                <div v-if="errors.username" class="text-danger mt-1">
                  {{ errors.username }}
                </div>
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">이메일</label>
                <input
                  type="email"
                  id="email"
                  v-model.trim="email"
                  class="form-control"
                  required
                />
                <div v-if="errors.email" class="text-danger mt-1">
                  {{ errors.email }}
                </div>
              </div>
              <div class="mb-3">
                <label for="password1" class="form-label">비밀번호</label>
                <input
                  type="password"
                  id="password1"
                  v-model.trim="password1"
                  class="form-control"
                  required
                  autocomplete="new-password"
                />
                <small class="form-text text-muted">
                  비밀번호는 최소 8자 이상, 숫자와 문자를 포함해야 합니다.
                </small>
                <div v-if="errors.password1" class="text-danger mt-1">
                  {{ errors.password1 }}
                </div>
              </div>
              <div class="mb-3">
                <label for="password2" class="form-label">비밀번호 확인</label>
                <input
                  type="password"
                  id="password2"
                  v-model.trim="password2"
                  class="form-control"
                  required
                  autocomplete="new-password"
                />
                <div v-if="errors.password2" class="text-danger mt-1">
                  {{ errors.password2 }}
                </div>
              </div>
              <div class="alert alert-danger" v-if="generalError">
                {{ generalError }}
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">회원가입</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const username = ref("");
const email = ref("");
const password1 = ref("");
const password2 = ref("");
const errors = ref({});
const generalError = ref("");

const handleSignUp = async () => {
  errors.value = {};
  generalError.value = "";

  // 기본 검증
  if (password1.value !== password2.value) {
    errors.value.password2 = "비밀번호가 일치하지 않습니다.";
    return;
  }
  if (password1.value.length < 8) {
    errors.value.password1 = "비밀번호는 최소 8자 이상이어야 합니다.";
    return;
  }
  if (!/\d/.test(password1.value) || !/[a-zA-Z]/.test(password1.value)) {
    errors.value.password1 = "비밀번호는 숫자와 문자를 포함해야 합니다.";
    return;
  }

  try {
    // 회원가입 요청
    await axios.post("http://127.0.0.1:8000/accounts/signup/", {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    });
    alert("회원가입이 완료되었습니다!");
    window.location.href = "/login"; // 로그인 페이지로 이동
  } catch (error) {
    if (error.response && error.response.data) {
      const data = error.response.data;
      if (data.username) {
        errors.value.username = data.username[0];
      }
      if (data.email) {
        errors.value.email = data.email[0];
      }
      if (data.password1) {
        errors.value.password1 = data.password1[0];
      }
    } else {
      generalError.value = "서버와의 통신에 문제가 발생했습니다.";
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
.card {
  border-radius: 0.5rem;
}
.card-title {
  font-size: 1.8rem;
  color: var(--primary-color);
}
</style>
