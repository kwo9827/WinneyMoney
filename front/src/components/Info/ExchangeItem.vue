<template>
  <div class="container">
    <h3>환율 계산기</h3>
    <!-- 국가 선택 드롭다운 -->
    <div class="filters">
      <label for="country">국가</label>
      <select id="country" v-model="inputCountry">
        <option value="">국가 선택</option>
        <option v-for="country in countries" :key="country" :value="country">
          {{ country }}
        </option>
      </select>
    </div>

    <!-- 금액 입력 -->
    <div class="filters">
      <label for="won">금액</label>
      <input 
        type="number" 
        id="won" 
        v-model="won" 
        placeholder="금액 입력" 
      />
    </div>

    <!-- 환율 정보 출력 -->
    <div class="result" v-if="formattedChangeMoney">
      <p>환전 결과: {{ formattedChangeMoney }}</p>
    </div>

    <!-- 계산하기 버튼 -->
    <form @submit.prevent="exchange">
      <button type="submit">계산하기</button>
    </form>
  </div>
</template>



<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useExchangeStore } from '@/stores/exchange';
import { useAccountStore } from '@/stores/accounts';

// 상태 정의
const exchangeStore = useExchangeStore();
const store = useAccountStore();

const changedMoney = ref(0)
const countries = exchangeStore.countries;
const countryCodes = exchangeStore.countryCodes;

const inputCountry = ref(''); // 선택된 국가
const won = ref(0); // 입력된 금액
const changeMoney = ref(null); // 환전 결과

// 계산된 환전 결과에 쉼표 추가
const formattedChangeMoney = computed(() => {
  return changedMoney.value ? changedMoney.value.toLocaleString() : '';
});

// 계산하기 함수
const exchange = () => {
  if (!inputCountry.value || !won.value) {
    alert('국가와 금액을 입력해주세요.');
    return;
  }

  const countryCode = countryCodes[inputCountry.value]; // 선택된 국가 코드 가져오기
  if (!countryCode) {
    alert('올바른 국가를 선택해주세요.');
    return;
  }

  // axios 요청
  axios({
    url: `${store.API_URL}/exchange/${countryCode}/${won.value}/`,
    method: 'GET',
  })
    .then((res) => {
      exchangeStore.getChange(res.data); // Store에 환율 정보 저장
      changeMoney.value = res.data; // 환전 결과 업데이트
      changedMoney.value = changeMoney.value.exchangeresult
    })
    .catch((err) => {
      console.error('환전 요청 실패:', err);
      alert('환전 요청 중 오류가 발생했습니다.');
    });
};
</script>


<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: #34495e;
  margin-bottom: 1rem;
}

.filters {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.filters label {
  font-size: 1rem;
  color: #34495e;
}

.filters input,
.filters select {
  flex: 1;
  margin-left: 1rem;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
}

.filters input:focus,
.filters select:focus {
  outline: none;
  border-color: #3498db;
}

.result {
  margin: 1rem 0;
  font-size: 1.2rem;
  color: #27ae60;
  text-align: center;
}

button {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  color: white;
  background-color: #3498db;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}
</style>
