<template>
  <div>
    <h3>주식 추가</h3>
    <div>
      <label for="ticker">주식 Ticker:</label>
      <input id="ticker" v-model="stock.ticker" placeholder="AAPL" />

      <label for="quantity">수량:</label>
      <input id="quantity" v-model.number="stock.quantity" placeholder="10" type="number" />

      <label for="purchase_price">구매 가격:</label>
      <input id="purchase_price" v-model.number="stock.purchase_price" placeholder="150.50" type="number" />

      <button @click="addStock">추가</button>
    </div>
    <ul>
      <li v-for="(item, index) in stocks" :key="index">
        {{ item.ticker }} - {{ item.quantity }}주 (구매가: {{ item.purchase_price }})
      </li>
    </ul>

    <h3>채권 추가</h3>
    <div>
      <label for="bond_name">채권 이름:</label>
      <input id="bond_name" v-model="bond.name" placeholder="채권 이름" />

      <label for="investment">투자 금액:</label>
      <input id="investment" v-model.number="bond.investment" placeholder="1000000.00" type="number" />

      <label for="yield_rate">수익률(%):</label>
      <input id="yield_rate" v-model.number="bond.yield_rate" placeholder="5.0" type="number" />

      <label for="maturity_date">만기일:</label>
      <input id="maturity_date" v-model="bond.maturity_date" placeholder="YYYY-MM-DD" type="date" />

      <button @click="addBond">추가</button>
    </div>
    <ul>
      <li v-for="(item, index) in bonds" :key="index">
        {{ item.name }} - {{ item.investment }}원 (수익률: {{ item.yield_rate }}%, 만기일: {{ item.maturity_date }})
      </li>
    </ul>

    <button @click="$emit('submit')">완료</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/accounts";
import axios from "axios";

const portfolioId = 1; // 포트폴리오 ID
const stocks = ref([]);
const bonds = ref([]);
const store = useAccountStore();
const token = store.token

const stock = ref({ ticker: "", quantity: 0, purchase_price: 0 });
const bond = ref({ name: "", investment: 0, yield_rate: 0, maturity_date: "" });

// 주식 추가 함수
const addStock = async () => {
  try {
    const response = await axios.post(
      `${store.API_URL}/portfolios/${portfolioId}/stocks/`,
      { stocks: [stock.value] },
      {
        headers: {
          Authorization: `Token ${token}`, // 인증 헤더
        },
      }
    );
    stocks.value.push({ ...stock.value });
    stock.value = { ticker: "", quantity: 0, purchase_price: 0 };
    alert("주식 추가 성공!");
  } catch (error) {
    console.error("주식 추가 실패:", error.response?.data || error.message);
    alert("주식 추가 실패! 다시 시도하세요.");
  }
};

// 채권 추가 함수
const addBond = async () => {
  try {
    const response = await axios.post(
      `${store.API_URL}/portfolios/${portfolioId}/bonds/`,
      bond.value,
      {
        headers: {
          Authorization: `Token ${token}`, // 인증 헤더
        },
      }
    );
    bonds.value.push({ ...bond.value });
    bond.value = { name: "", investment: 0, yield_rate: 0, maturity_date: "" };
    alert("채권 추가 성공!");
  } catch (error) {
    console.error("채권 추가 실패:", error.response?.data || error.message);
    alert("채권 추가 실패! 다시 시도하세요.");
  }
};
</script>
