<template>
  <div class="container mt-5">
    <!-- 사용자 프로필 정보 -->
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">사용자 프로필</h2>
            <!-- 프로필 이미지 -->
            <div class="text-center mb-4">
              <img 
                :src="accountStore.profileImage || 'https://via.placeholder.com/150'" 
                alt="프로필 이미지" 
                class="rounded-circle profile-image"
              >
            </div>
            <!-- 사용자 정보 -->
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <strong>사용자명:</strong> {{ accountStore.username }}
              </li>
              <li class="list-group-item">
                <strong>이메일:</strong> {{ accountStore.email }}
              </li>
              <li class="list-group-item">
                <strong>이름:</strong> {{ accountStore.lastName }} {{ accountStore.firstName }}
              </li>
              <li class="list-group-item">
                <strong>팔로워:</strong> {{ accountStore.followersCount }}
                <button class="btn btn-link p-0 ms-2" @click="toggleFollowers">
                  보기
                </button>
              </li>
              <li class="list-group-item">
                <strong>팔로잉:</strong> {{ accountStore.followingCount }}
                <button class="btn btn-link p-0 ms-2" @click="toggleFollowing">
                  보기
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- 포트폴리오 목록 -->
    <div class="row mt-4">
      <div class="col-12">
        <h3 class="text-center">내 포트폴리오</h3>
        <div class="d-flex flex-wrap justify-content-center">
          <div 
            v-for="portfolio in portfolioStore.portfolios" 
            :key="portfolio.id" 
            class="portfolio-card card m-2 p-3"
          >
            <h4>{{ portfolio.name }}</h4>
            <p><strong>총 투자:</strong> {{ portfolio.total_investment.toLocaleString() }}₩</p>
            <p><strong>변동성:</strong> {{ portfolio.volatility ? portfolio.volatility.toFixed(2) + '%' : 'N/A' }}</p>
            <button 
              class="btn btn-primary w-100 mt-2"
              @click="viewPortfolioDetail(portfolio.id)"
            >
              자세히 보기
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 팔로워 및 팔로잉 리스트 모달 -->
    <FollowListModal
      v-if="showModal"
      :type="modalType"
      :list="modalList"
      @close="showModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accounts";
import { usePortfolioStore } from "@/stores/portfolio";
import FollowListModal from "@/components/accounts/FollowListModal.vue";

const router = useRouter();
const accountStore = useAccountStore();
const portfolioStore = usePortfolioStore();

const showModal = ref(false);
const modalType = ref(""); // 'followers' 또는 'following'
const modalList = ref([]);

// 팔로워 목록 보기
const toggleFollowers = () => {
  modalType.value = "followers";
  modalList.value = accountStore.followers;
  showModal.value = true;
};

// 팔로잉 목록 보기
const toggleFollowing = () => {
  modalType.value = "following";
  modalList.value = accountStore.following;
  showModal.value = true;
};

// 포트폴리오 상세 보기
const viewPortfolioDetail = (portfolioId) => {
  // 포트폴리오 상세 페이지로 이동
  router.push({ name: "RecommendationView", params: { portfolioId } });
};

// 데이터 로드
const fetchData = async () => {
  try {
    await accountStore.getUserProfile(); // 사용자 프로필 가져오기
    await portfolioStore.fetchUserPortfolios(); // 사용자 포트폴리오 가져오기
  } catch (error) {
    console.error("데이터를 가져오는 중 오류가 발생했습니다.", error);
  }
};

onMounted(fetchData);
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

/* 포트폴리오 카드 스타일 */
.portfolio-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  width: 300px;
}

.portfolio-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
</style>
