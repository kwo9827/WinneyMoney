<template>
  <v-container class="step-container">
    <v-card class="card" width="100%" elevation="2">
      <v-card-title>
        <h2>보유한 주식 입력</h2>
      </v-card-title>
      <v-card-text>
        <!-- 주식 Ticker 입력 -->
        <v-text-field
          label="주식 Ticker"
          v-model="searchQuery"
          placeholder="예: AAPL"
          outlined
          color="primary"
          :error-messages="tickerError"
        ></v-text-field>

        <!-- 추천 항목 표시 -->
        <div v-if="searchResults.length" class="suggestions">
          <p>이게 맞나요?</p>
          <v-chip-group column>
            <v-chip
              v-for="(result, index) in searchResults.slice(0, 3)"
              :key="index"
              @click="selectSuggestion(result.ticker)"
              outlined
            >
              {{ result.name }} ({{ result.ticker }})
            </v-chip>
          </v-chip-group>
        </div>

        <!-- 1주당 구매 가격 입력 -->
        <v-text-field
          label="1주당 구매 가격 (₩)"
          v-model="formattedPrice"
          placeholder="예: 150.50"
          outlined
          color="primary"
          @input="validatePurchasePrice"
        ></v-text-field>

        <!-- 총 구매 금액 입력 -->
        <v-text-field
          label="총 구매 금액 (₩)"
          v-model="formattedInvestment"
          placeholder="예: 1500000"
          outlined
          color="primary"
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
          ></v-text-field>
          <v-text-field
            label="1주당 구매 가격 (₩)"
            v-model="editingStock.purchase_price"
            outlined
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
import axios from "axios";
import { usePortfolioStore } from "@/stores/portfolio";

const portfolioStore = usePortfolioStore();

const addedStocks = computed(() =>
  portfolioStore.portfolio.stocks.flatMap((group) => group.added_stocks || [])
);

const searchQuery = ref(""); // 검색 입력값
const searchResults = ref([]); // 검색 결과
const isLoading = ref(false); // 로딩 상태

const formattedPrice = ref(""); // 가격 포맷팅
const formattedInvestment = ref(""); // 투자 금액 포맷팅

const tickerError = ref(""); // 오류 메시지
const ticker = ref(""); // 선택된 Ticker

const editDialog = ref(false);
const editingStock = ref({});

// 검색 결과 API 호출
const fetchSearchResults = async (query) => {
  if (!query?.trim()) {
    searchResults.value = [];
    return;
  }

  isLoading.value = true;
  try {
    const response = await axios.get("http://127.0.0.1:8000/market/search/", {
      params: { query },
    });
    searchResults.value = response.data;
  } catch (error) {
    console.error("검색 API 호출 실패:", error.response?.data || error.message);
    searchResults.value = [];
  } finally {
    isLoading.value = false;
  }
};

// `searchQuery` 값 변경 시 API 호출
watch(
  searchQuery,
  (newQuery) => {
    fetchSearchResults(newQuery);
  }
);

// 추천 항목 선택
const selectSuggestion = (selectedTicker) => {
  ticker.value = selectedTicker; // 선택된 Ticker 저장
  searchQuery.value = selectedTicker; // 검색 입력란에 반영
};

// 1주당 구매 가격 입력값 포맷팅
const validatePurchasePrice = () => {
  const value = formattedPrice.value.replace(/[^\d.]/g, "");
  formattedPrice.value = value ? parseFloat(value).toLocaleString() : "";
};

// 총 투자 금액 입력값 포맷팅
const validateTotalInvestment = () => {
  const value = formattedInvestment.value.replace(/[^\d]/g, "");
  formattedInvestment.value = value ? parseInt(value, 10).toLocaleString() : "";
};

// 주식 추가 함수
const addStock = async () => {
  if (!ticker.value || !formattedPrice.value || !formattedInvestment.value) {
    tickerError.value = "모든 필드를 올바르게 입력해주세요.";
    return;
  }

  // 중복 체크
  const isDuplicate = addedStocks.value.some(
    (existingStock) => existingStock.ticker === ticker.value
  );

  if (isDuplicate) {
    tickerError.value = "이미 추가된 주식입니다.";
    return;
  }

  try {
    const stock = {
      ticker: ticker.value,
      purchase_price: parseFloat(formattedPrice.value.replace(/,/g, "")),
      total_investment: parseInt(formattedInvestment.value.replace(/,/g, ""), 10),
    };

    const payload = {stocks: [stock]}
    // 스토어에 추가 요청
    await portfolioStore.addStock(payload);
    alert("주식 추가 성공!");

    // 초기화
    ticker.value = "";
    searchQuery.value = "";
    formattedPrice.value = "";
    formattedInvestment.value = "";
    searchResults.value = [];
    tickerError.value = "";

  } catch (error) {
    console.error("주식 추가 실패:", error);
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
    // addedStocks.value = portfolio.stocks.flatMap((group) => group.added_stocks || []);
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

.suggestions {
  margin-top: 10px;
}

.suggestions p {
  font-size: 14px;
  color: #757575;
}

.v-chip-group {
  margin-top: 10px;
}
</style>
