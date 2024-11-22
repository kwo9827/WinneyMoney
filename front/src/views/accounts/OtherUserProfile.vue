<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">{{ profile.username }}님의 프로필</h2>
            <!-- 프로필 이미지 -->
            <div class="text-center mb-4">
              <img
                :src="profile.profile_image || 'https://via.placeholder.com/150'"
                alt="프로필 이미지"
                class="rounded-circle profile-image"
              >
            </div>
            <!-- 사용자 정보 -->
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <strong>사용자명:</strong> {{ profile.username }}
              </li>
              <li class="list-group-item">
                <strong>이메일:</strong> {{ profile.email }}
              </li>
              <li class="list-group-item">
                <strong>팔로워:</strong> {{ profile.followers_count }}
              </li>
              <li class="list-group-item">
                <strong>팔로잉:</strong> {{ profile.following_count }}
              </li>
            </ul>
            <!-- 팔로우 버튼 -->
            <div class="text-center mt-3">
              <button
                class="btn btn-primary"
                @click="toggleFollow"
              >
                {{ isFollowing ? '팔로우 취소' : '팔로우' }}
              </button>
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
import { useRoute } from 'vue-router'

const profile = ref({})
const isFollowing = ref(false)
const store = useAccountStore()
const route = useRoute()

// 프로필 데이터 가져오기
const fetchProfile = () => {
  const username = route.params.username // URL에서 username 추출
  store.getOtherUserProfile(username).then((data) => {
    profile.value = data.profile
    isFollowing.value = data.is_following
  }).catch((err) => {
    console.error('프로필 가져오기 실패:', err)
  })
}

// 팔로우/언팔로우 토글
const toggleFollow = () => {
  store.toggleFollow(profile.value.username).then(() => {
    isFollowing.value = !isFollowing.value
    if (isFollowing.value) {
      profile.value.followers_count++
    } else {
      profile.value.followers_count--
    }
  })
}

// 컴포넌트 마운트 시 프로필 가져오기
onMounted(fetchProfile)
</script>

<style scoped>
/* 기존 스타일 유지 */
.profile-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border: 3px solid #3498db;
}
</style>
