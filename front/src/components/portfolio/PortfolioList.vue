<!-- <template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">내 포트폴리오</h2>
            <!-- 포트폴리오 데이터 표시 -->
            <ul v-if="portfolios.length" class="list-group">
              <li
                v-for="portfolio in portfolios"
                :key="portfolio.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <strong>{{ portfolio.name }}</strong>
                <span>{{ portfolio.total_investment }}원</span>
              </li>
            </ul>
            <!-- 포트폴리오가 없을 경우 -->
            <p v-else class="text-center text-muted">포트폴리오가 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { usePortfolioStore } from "@/stores/portfolio";
import { useAccountStore } from "@/stores/counter";
import { ref, onMounted } from "vue";
import { useAccountStore } from "@/stores/accounts";

// Pinia Store와 상태 선언
const portfolioStore = usePortfolioStore();
const store = useAccountStore();
const portfolios = ref([]); // Vue의 ref로 상태 선언

// API 호출 및 데이터 관리
onMounted(() => {
  const token = store.token
  axios({
    url: `${store.API_URL}/portfolios/`, // API URL
    method: "GET",
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then((res) => {
      console.log(res)
      portfolioStore.getPortfolios(res.data); // Store에 데이터 저장
      portfolios.value = portfolioStore.portfolios; // Store의 상태를 로컬 상태에 반영
    })
    .catch((error) => {
      console.error("포트폴리오 데이터를 가져오지 못했습니다:", error);
    });
});
</script>

<style scoped>
.list-group-item {
  cursor: pointer;
  transition: background-color 0.3s;
}
.list-group-item:hover {
  background-color: #f8f9fa;
}
</style> -->
