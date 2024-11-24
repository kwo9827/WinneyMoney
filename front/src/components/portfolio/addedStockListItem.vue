<template>
  <v-card outlined elevation="1" class="stock-card">
    <v-card-title>
      <strong>{{ stock.ticker }}</strong>
    </v-card-title>
    <v-card-subtitle>
      총 {{ parseFloat(stock.total_investment || 0).toLocaleString() }}원
    </v-card-subtitle>
    <v-card-text>
      1주당 구매가: {{ parseFloat(stock.purchase_price || 0).toLocaleString() }}원<br />
      변동성: {{ stock.volatility?.toFixed(2) || "데이터 없음" }}
    </v-card-text>
    <v-card-actions>
      <v-btn small text color="blue" @click="openEditDialog">수정</v-btn>
      <v-btn small text color="red" @click="removeStock">삭제</v-btn>
    </v-card-actions>

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
          <v-btn text color="red" @click="closeEditDialog">취소</v-btn>
          <v-btn text color="primary" @click="updateStock">저장</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  stock: Object,
});

const emit = defineEmits(["remove-stock", "update-stock"]);

// Dialog 상태 및 수정용 데이터
const editDialog = ref(false);
const editingStock = ref({ ...props.stock });

// 수정 Dialog 열기
const openEditDialog = () => {
  editingStock.value = { ...props.stock }; // 원본 데이터를 복사
  editDialog.value = true;
};

// Dialog 닫기
const closeEditDialog = () => {
  editDialog.value = false;
};

// 수정 저장
const updateStock = () => {
  emit("update-stock", editingStock.value);
  closeEditDialog();
};

// 삭제
const removeStock = () => {
  emit("remove-stock", props.stock.id);
};
</script>

<style scoped>
.stock-card {
  margin-bottom: 20px;
}
</style>
