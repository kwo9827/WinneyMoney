<template>
  <v-container class="step-container">
    <v-card class="card" width="100%"elevation="2">
      <v-card-title>
        <h2>암호화폐 추가</h2>
      </v-card-title>
      <v-card-text>
        <!-- 암호화폐 심볼 입력 -->
        <v-text-field
          label="암호화폐 심볼"
          v-model="searchQuery"
          placeholder="예: BTC"
          outlined
          color="primary"
          :error-messages="symbolError"
        ></v-text-field>

        <!-- 추천 항목 표시 -->
        <div v-if="searchResults.length" class="suggestions">
          <p>이게 맞나요?</p>
          <v-chip-group column>
            <v-chip
              v-for="(result, index) in searchResults.slice(0, 3)"
              :key="index"
              @click="selectSuggestion(result.symbol)"
              outlined
            >
              {{ result.symbol }}
            </v-chip>
          </v-chip-group>
        </div>

        <!-- 1단위 구매 가격 입력 -->
        <v-text-field
          label="1단위 구매 가격 (₩)"
          v-model="formattedPrice"
          placeholder="50000.00"
          outlined
          color="primary"
          @input="validatePurchasePrice"
        ></v-text-field>

        <!-- 총 구매 금액 입력 -->
        <v-text-field
          label="총 구매 금액 (₩)"
          v-model="formattedInvestment"
          placeholder="500000.00"
          outlined
          color="primary"
          @input="validateTotalInvestment"
        ></v-text-field>

        <!-- 암호화폐 추가 버튼 -->
        <v-btn @click="addCrypto" color="primary" class="mt-4">암호화폐 추가</v-btn>
      
        <!-- 추가된 암호화폐 리스트 -->
        <v-alert v-if="cryptos.length" type="info" class="mt-4">
          <v-row dense>
            <v-col
              v-for="(crypto, index) in cryptos"
              :key="crypto.id || index"
              cols="12"
              md="6"
            >
              <v-card outlined elevation="1" class="crypto-card">
                <v-card-title>
                  <strong>{{ crypto.symbol }}</strong>
                </v-card-title>
                <v-card-subtitle>
                  총 {{ parseFloat(crypto.total_investment || 0).toLocaleString() }}원
                </v-card-subtitle>
                <v-card-text>
                  구매가: {{ parseFloat(crypto.purchase_price || 0).toLocaleString() }}원<br />
                  현재가: {{ crypto.current_value }}
                  <br>
                  변동성: {{ crypto.volatility?.toFixed(2) || "데이터 없음" }}
                </v-card-text>
                <v-card-actions>
                  <v-btn small text color="blue" @click="openEditDialog(crypto)">수정</v-btn>
                  <v-btn small text color="red" @click="deleteCrypto(crypto.id)">삭제</v-btn>
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
          <span>암호화폐 수정</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="총 구매 금액 (₩)"
            v-model="editingCrypto.total_investment"
            outlined
          ></v-text-field>
          <v-text-field
            label="구매당시 구매 가격 (₩)"
            v-model="editingCrypto.purchase_price"
            outlined
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="red" @click="editDialog = false">취소</v-btn>
          <v-btn text color="primary" @click="updateCrypto">수정</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  <v-row justify="space-between" class="mt-5">
    <v-col cols='6'>
      <v-btn color="secondary" outlined @click="$emit('prev')">
        이전
      </v-btn>
    </v-col>
    <v-col cols='6'>
      <v-btn @click="$emit('submit')" color="success">다음</v-btn>
    </v-col>
  </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import axios from "axios";
import { usePortfolioStore } from "@/stores/portfolio";

const portfolioStore = usePortfolioStore();

const cryptos = computed(() =>
  portfolioStore.portfolio.cryptocurrencies.flatMap((group) => group.added_cryptos || [])
);

const searchQuery = ref(""); // 검색 입력값
const searchResults = ref([]); // 검색 결과
const isLoading = ref(false); // 로딩 상태

const formattedPrice = ref(""); // 가격 포맷팅
const formattedInvestment = ref(""); // 투자 금액 포맷팅

const symbolError = ref(""); // 오류 메시지
const selectedSymbol = ref(""); // 선택된 심볼

const editDialog = ref(false);
const editingCrypto = ref({});

// 검색 결과 API 호출
const fetchSearchResults = async (query) => {
  if (!query?.trim()) {
    searchResults.value = [];
    return;
  }

  isLoading.value = true;
  try {
    const response = await axios.get("http://127.0.0.1:8000/market/search/coin/", {
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
const selectSuggestion = (symbol) => {
  selectedSymbol.value = symbol; // 선택된 심볼 저장
  searchQuery.value = symbol; // 검색 입력란에 반영
};

// 1단위 구매 가격 포맷팅
const validatePurchasePrice = () => {
  const value = formattedPrice.value.replace(/[^\d.]/g, "");
  formattedPrice.value = value ? parseFloat(value).toLocaleString() : "";
};

// 총 구매 금액 포맷팅
const validateTotalInvestment = () => {
  const value = formattedInvestment.value.replace(/[^\d]/g, "");
  formattedInvestment.value = value ? parseInt(value, 10).toLocaleString() : "";
};

// 암호화폐 추가
const addCrypto = async () => {
  if (!selectedSymbol.value || !formattedPrice.value || !formattedInvestment.value) {
    symbolError.value = "모든 필드를 올바르게 입력해주세요.";
    return;
  }

  const crypto = {
    symbol: selectedSymbol.value,
    purchase_price: parseFloat(formattedPrice.value.replace(/,/g, "")),
    total_investment: parseInt(formattedInvestment.value.replace(/,/g, ""), 10),
  };

  try {
    await portfolioStore.addCrypto({ cryptos: [crypto] });
    alert("암호화폐가 추가되었습니다.");
    resetForm();
  } catch (error) {
    symbolError.value = "추가 실패: " + error.message;
  }
};

// 폼 초기화
const resetForm = () => {
  selectedSymbol.value = "";
  searchQuery.value = "";
  formattedPrice.value = "";
  formattedInvestment.value = "";
  searchResults.value = [];
  symbolError.value = "";
};

// 수정 Dialog 열기
const openEditDialog = (crypto) => {
  editingCrypto.value = { ...crypto };
  editDialog.value = true;
};

// 암호화폐 수정
const updateCrypto = async () => {
  try {
    await portfolioStore.updateCrypto(editingCrypto.value);
    editDialog.value = false;
    alert("암호화폐가 수정되었습니다.");
  } catch (error) {
    alert("수정 실패: " + error.message);
  }
};

// 암호화폐 삭제
const deleteCrypto = async (cryptoId) => {
  try {
    await portfolioStore.deleteCrypto(cryptoId);
    alert("암호화폐가 삭제되었습니다.");
  } catch (error) {
    alert("삭제 실패: " + error.message);
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

.v-btn {
  width: auto;
  min-width: 120px;
}
</style>
