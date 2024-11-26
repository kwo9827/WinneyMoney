<template>
  <v-container class="step-container">
    <v-card class="card" elevation="2">
      <v-card-title>
        <h2>주식 추가</h2>
      </v-card-title>
      <v-card-text>
        <!-- 주식 Ticker 입력 -->
        <v-text-field
          label="주식 Ticker"
          v-model="stock.ticker"
          placeholder="예: AAPL"
          outlined
          color="primary"
          clearable
          :error-messages="tickerError"
        ></v-text-field>

        <!-- 1주당 구매 가격 입력 -->
        <v-text-field
          label="1주당 구매 가격 (₩)"
          v-model="formattedPrice"
          placeholder="예: 150.50"
          outlined
          color="primary"
          clearable
          @input="validatePurchasePrice"
        ></v-text-field>

        <!-- 총 구매 금액 입력 -->
        <v-text-field
          label="총 구매 금액 (₩)"
          v-model="formattedInvestment"
          placeholder="예: 1500000"
          outlined
          color="primary"
          clearable
          @input="validateTotalInvestment"
        ></v-text-field>

        <!-- 주식 추가 버튼 -->
        <v-btn @click="addStock" color="primary" class="mt-4">주식 추가</v-btn>


        <!-- 추가된 주식 리스트 -->
        <v-alert v-if="addedStocks.length" type="info" class="mt-4">
          <v-row dense>
            <v-col
              v-for="(stock, index) in addedStocks"
              :key="stock.id || index"
              cols="12"
              md="6"
            >
              <v-card outlined elevation="1" class="stock-card">
                <v-card-title>
                  <strong>{{ stock.ticker }}</strong>
                </v-card-title>
                <v-card-subtitle>
                  총 {{ parseFloat(stock.total_investment || 0).toLocaleString() }}원
                </v-card-subtitle>
                <v-card-text>
                  1주당 구매가: {{ parseFloat(stock.purchase_price || 0).toLocaleString() }}원<br />
                  현재가: {{ stock.current_value }} 
                  <br>
                  변동성: {{ stock.volatility?.toFixed(2) || "데이터 없음" }}
                </v-card-text>
                <v-card-actions>
                  <v-btn small text color="blue" @click="openEditDialog(stock)">수정</v-btn>
                  <v-btn small text color="red" @click="deleteStock(stock.id)">삭제</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-alert>
      </v-card-text>
    </v-card>

    <!-- 수정 Dialog -->
    <v-dialog v-model="editDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span>주식 수정</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="총 구매 금액 (₩)"
            v-model="editingStock.total_investment"
            outlined
            clearable
          ></v-text-field>
          <v-text-field
            label="1주당 구매 가격 (₩)"
            v-model="editingStock.purchase_price"
            outlined
            clearable
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="red" @click="editDialog = false">취소</v-btn>
          <v-btn text color="primary" @click="updateStock">수정</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 다음 단계 버튼 -->
    <v-btn @click="$emit('next')" color="success" class="mt-5">다음</v-btn>
  </v-container>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";

const portfolioStore = usePortfolioStore();
const portfolio = portfolioStore.portfolio;

// **반응형 변수 addedStocks 정의**
// const addedStocks = computed(() => 
//   portfolioStore.portfolio.stocks
// )

const addedStocks = computed(() =>
  portfolioStore.portfolio.stocks.flatMap((group) => group.added_stocks || [])
);
const newdata = ref([])
// **watch로 portfolio.stocks 감시**
watch(
  () => portfolio.stocks,
  (newStocks) => {
    // 모든 주식을 addedStocks에 다시 저장
    // addedStocks.value = newStocks.flatMap((group) => group.added_stocks || []);
    newdata.value=newStocks

  },
  { immediate: true, deep: true }
);

const stock = ref({ ticker: "", purchase_price: 0, total_investment: 0 });
const tickerError = ref("");
const editDialog = ref(false);
const editingStock = ref({});

const formattedPrice = ref("");
const formattedInvestment = ref("");

// 숫자 포맷팅 로직
const validatePurchasePrice = () => {
  const value = formattedPrice.value.replace(/[^\d.]/g, "");
  stock.value.purchase_price = parseFloat(value) || 0;
  formattedPrice.value = stock.value.purchase_price
    ? stock.value.purchase_price.toLocaleString()
    : "";
};

const validateTotalInvestment = () => {
  const value = formattedInvestment.value.replace(/[^\d]/g, "");
  stock.value.total_investment = parseInt(value, 10) || 0;
  formattedInvestment.value = stock.value.total_investment
    ? stock.value.total_investment.toLocaleString()
    : "";
};

// 주식 추가 함수
const addStock = async () => {
  if (!stock.value.ticker || stock.value.purchase_price <= 0 || stock.value.total_investment <= 0) {
    tickerError.value = "모든 필드를 올바르게 입력해주세요.";
    return;
  }

  const isDuplicate = addedStocks.value.some(
    (existingStock) => existingStock.ticker === stock.value.ticker
  );

  if (isDuplicate) {
    tickerError.value = "이미 추가된 주식입니다.";
    return;
  }

  try {
    const payload = { stocks: [stock.value] }; // `stocks` 배열로 래핑
    console.log("전송 데이터:", payload); // 디버깅용 로그
    await portfolioStore.addStock(payload); // 스토어 액션 호출
    stock.value = { ticker: "", purchase_price: 0, total_investment: 0 }; // 입력 초기화
    tickerError.value = ""; // 오류 초기화
    formattedPrice.value = "";
    formattedInvestment.value = "";
    alert("주식 추가 성공!");
  } catch (error) {
    tickerError.value = error.message || "주식 추가 실패! 다시 시도하세요.";
  }
};

// 수정 Dialog 열기
const openEditDialog = (item) => {
  editingStock.value = { ...item };
  editDialog.value = true;
};

// 주식 수정
const updateStock = async () => {
  try {
    await portfolioStore.updateStock(editingStock.value);
    editDialog.value = false;
    alert("주식이 수정되었습니다.");
    console.log(portfolioStore.portfolio)
  } catch (error) {
    alert("수정 실패!");
  }
};

// 주식 삭제
const deleteStock = async (stockId) => {
  try {
    await portfolioStore.deleteStock(stockId);

    // 삭제 후 addedStocks를 업데이트
    addedStocks.value = portfolio.stocks.flatMap((group) => group.added_stocks || []);
    alert("삭제 완료!");
  } catch (error) {
    alert("삭제 실패!");
  }
};
</script>

<style scoped>
.step-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  max-width: 600px;
}

.card {
  padding: 20px;
  width: 100%;
}

.mt-4 {
  margin-top: 1rem;
}

.mt-5 {
  margin-top: 1.5rem;
}

.stock-card {
  margin-bottom: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stock-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.v-btn {
  font-size: 0.85rem;
}
</style>
