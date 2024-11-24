<template>
  <v-container class="step-container">
    <v-card class="card" elevation="2">
      <v-card-title>
        <h2>암호화폐 추가</h2>
      </v-card-title>
      <v-card-text>
        <!-- 암호화폐 이름 입력 -->
        <v-text-field
          label="암호화폐 이름"
          v-model="crypto.name"
          placeholder="Bitcoin"
          outlined
          color="primary"
          clearable
        ></v-text-field>

        <!-- 암호화폐 심볼 입력 -->
        <v-text-field
          label="암호화폐 심볼"
          v-model="crypto.symbol"
          placeholder="BTC"
          outlined
          color="primary"
          clearable
        ></v-text-field>

        <!-- 1단위 구매 가격 입력 -->
        <v-text-field
          label="1단위 구매 가격 (₩)"
          v-model="formattedPrice"
          placeholder="50000.00"
          outlined
          color="primary"
          clearable
          @input="validatePurchasePrice"
        ></v-text-field>

        <!-- 총 구매 금액 입력 -->
        <v-text-field
          label="총 구매 금액 (₩)"
          v-model="formattedInvestment"
          placeholder="500000.00"
          outlined
          color="primary"
          clearable
          @input="validateTotalInvestment"
        ></v-text-field>

        <!-- 암호화폐 추가 버튼 -->
        <v-btn @click="addCrypto" color="primary" class="mt-4">암호화폐 추가</v-btn>
       
       {{ cryptos }}
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
                  <strong>{{ crypto.name }} {{ crypto.symbol }}</strong>
                </v-card-title>
                <v-card-subtitle>
                  총 {{ parseFloat(crypto.total_investment || 0).toLocaleString() }}원
                </v-card-subtitle>
                <v-card-text>
                  1단위 구매가: {{ parseFloat(crypto.purchase_price || 0).toLocaleString() }}원<br />
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
            clearable
          ></v-text-field>
          <v-text-field
            label="1단위 구매 가격 (₩)"
            v-model="editingCrypto.purchase_price"
            outlined
            clearable
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="red" @click="editDialog = false">취소</v-btn>
          <v-btn text color="primary" @click="updateCrypto">수정</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 다음 단계 버튼 -->
    <v-btn @click="$emit('submit')" color="success" class="mt-5">다음</v-btn>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";
import { usePortfolioStore } from "@/stores/portfolio";

const portfolioStore = usePortfolioStore();

// 암호화폐 데이터와 관련된 반응형 변수 정의
const crypto = ref({
  name: "",
  symbol: "",
  purchase_price: 0,
  total_investment: 0,
});

const editingCrypto = ref({});
const editDialog = ref(false);

const formattedPrice = ref("");
const formattedInvestment = ref("");

const cryptos = computed(() => 
  portfolioStore.portfolio.cryptocurrencies.flatMap((group) => group.added_cryptos || [])
);

// 1단위 구매 가격 포맷팅
const validatePurchasePrice = () => {
  const value = formattedPrice.value.replace(/[^\d.]/g, "");
  crypto.value.purchase_price = parseFloat(value) || 0;
  formattedPrice.value = crypto.value.purchase_price
    ? crypto.value.purchase_price.toLocaleString()
    : "";
};

// 총 구매 금액 포맷팅
const validateTotalInvestment = () => {
  const value = formattedInvestment.value.replace(/[^\d]/g, "");
  crypto.value.total_investment = parseInt(value, 10) || 0;
  formattedInvestment.value = crypto.value.total_investment
    ? crypto.value.total_investment.toLocaleString()
    : "";
};

// 암호화폐 추가
const addCrypto = async () => {
  if (
    !crypto.value.name ||
    !crypto.value.symbol ||
    crypto.value.purchase_price <= 0 ||
    crypto.value.total_investment <= 0
  ) {
    alert("모든 필드를 올바르게 입력해주세요.");
    return;
  }

  try {
    const payload = { cryptos: [crypto.value] }; // `cryptos` 배열로 래핑
    await portfolioStore.addCrypto(payload); // store에서 추가
    crypto.value = { name: "", symbol: "", purchase_price: 0, total_investment: 0 }; // 입력 초기화
    formattedPrice.value = "";
    formattedInvestment.value = "";
    alert("암호화폐가 추가되었습니다.");
  } catch (error) {
    alert("추가 실패: " + error.message);
  }
};

// 암호화폐 삭제
const deleteCrypto = async (cryptoId) => {
  try {
    await portfolioStore.deleteCrypto(cryptoId); // store에서 삭제
    alert("암호화폐가 삭제되었습니다.");
  } catch (error) {
    alert("삭제 실패: " + error.message);
  }
};

// 수정 Dialog 열기
const openEditDialog = (crypto) => {
  editingCrypto.value = { ...crypto };
  editDialog.value = true;
};

// 암호화폐 수정
const updateCrypto = async () => {
  try {
    await portfolioStore.updateCrypto(editingCrypto.value); // store에서 수정
    editDialog.value = false;
    alert("암호화폐가 수정되었습니다.");
  } catch (error) {
    alert("수정 실패: " + error.message);
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

.crypto-card {
  margin-bottom: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.crypto-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.v-btn {
  font-size: 0.85rem;
}
</style>
