import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('accounts', () => {
  const API_URL = 'http://127.0.0.1:8000'

  // 상태 변수
  const token = ref(null)
  const username = ref('')
  const email = ref('')
  const firstName = ref('')
  const lastName = ref('')
  const profileImage = ref(null)

  // 로그인 상태 확인
  const isLogin = computed(() => token.value !== null)

  const router = useRouter()

  // 회원가입
  const signUp = function (payload) {
    const { username, email, password1, password2 } = payload

    return axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: { username, email, password1, password2 },
    })
      .then((res) => {
        console.log('회원가입 성공:', res.data)
        const password = password1
        return logIn({ username, password }) // 회원가입 후 자동 로그인
      })
      .catch((err) => {
        console.error('회원가입 실패:', err.response?.data)
      })
  }

  // 로그인
  const logIn = function (payload) {
    const { username: loginUsername, password } = payload
  
    return axios({
      method: 'post',
      url: `${API_URL}/accounts/auth/login/`,
      data: { username: loginUsername, password },
    })
      .then((res) => {
        token.value = res.data.key
        username.value = loginUsername
        console.log('로그인 성공: 토큰', token.value) // 여기에 토큰 값 확인
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.error('로그인 실패:', err.response?.data)
      })
  }
  
  // 로그아웃
  const logOut = function () {
    return axios({
      method: 'post',
      url: `${API_URL}/accounts/auth/logout/`,
      headers: { Authorization: `Token ${token.value}` },
    })
      .then(() => {
        token.value = null
        username.value = ''
        router.push({ name: 'HomeView' })
      })
      .catch((err) => {
        console.error('로그아웃 실패:', err.response?.data)
      })
  }

  // 회원탈퇴
  const deleteAccount = function () {
    return axios({
      method: 'delete',
      url: `${API_URL}/accounts/delete/`,
      headers: { Authorization: `Token ${token.value}` },
    })
      .then(() => {
        token.value = null
        username.value = ''
        router.push({ name: 'HomeView' })
      })
      .catch((err) => {
        console.error('회원탈퇴 실패:', err.response?.data)
        alert('회원탈퇴에 실패했습니다. 다시 시도해주세요.')
      })
  }

  // 회원 프로필 가져오기
  const getUserProfile = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/accounts/auth/user/`,
      headers: { Authorization: `Token ${token.value}` },
    })
      .then((res) => {
        const data = res.data
        email.value = data.email
        firstName.value = data.first_name
        lastName.value = data.last_name
        profileImage.value = data.profile_image
      })
      .catch((err) => {
        console.error('프로필 정보 가져오기 실패:', err.response?.data)
      })
  }

  // 회원정보 변경
  const updateProfile = function (payload) {
    return axios({
      method: 'put',
      url: `${API_URL}/accounts/auth/user/`,
      headers: { Authorization: `Token ${token.value}` },
      data: payload,
    })
      .then((res) => {
        const data = res.data
        email.value = data.email
        firstName.value = data.first_name
        lastName.value = data.last_name
        profileImage.value = data.profile_image
        router.push({ name: 'ProfileView' })
      })
      .catch((err) => {
        console.error('프로필 업데이트 실패:', err.response?.data)
        alert('프로필 업데이트에 실패했습니다. 다시 시도해주세요.')
      })
  }

  // 비밀번호 찾기 (이메일로 재설정 링크 전송)
  const resetPassword = function (email) {
    return axios({
      method: 'post',
      url: `${API_URL}/accounts/auth/password/reset/`,
      data: { email },
    })
      .then((res) => {
        console.log('비밀번호 재설정 이메일 전송 성공:', res.data)
        alert('비밀번호 재설정 이메일이 전송되었습니다. 이메일을 확인해주세요.')
      })
      .catch((err) => {
        console.error('비밀번호 재설정 이메일 전송 실패:', err.response?.data)
        alert('이메일 전송에 실패했습니다. 다시 시도해주세요.')
      })
  }

  // 비밀번호 변경
  const changePassword = function (payload) {
    const { old_password, new_password1, new_password2 } = payload

    return axios({
      method: 'post',
      url: `${API_URL}/accounts/auth/password/change/`,
      headers: { Authorization: `Token ${token.value}` },
      data: { old_password, new_password1, new_password2 },
    })
      .then((res) => {
        console.log('비밀번호 변경 성공:', res.data)
        alert('비밀번호가 성공적으로 변경되었습니다.')
        router.push({ name: 'ProfileView' })
      })
      .catch((err) => {
        console.error('비밀번호 변경 실패:', err.response?.data)
        alert('비밀번호 변경에 실패했습니다. 다시 시도해주세요.')
      })
  }

  return {
    API_URL,
    token,
    username,
    email,
    firstName,
    lastName,
    profileImage,
    isLogin,
    signUp,
    logIn,
    logOut,
    deleteAccount,
    getUserProfile,
    updateProfile,
    resetPassword,
    changePassword,
  }
}, { persist: true })
